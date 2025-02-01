import datetime
import json
import os

import pandas as pd
import requests
from dotenv import load_dotenv
import finnhub


load_dotenv()


def get_info(date: str) -> None:
    """ Принимает дату в формате: YYYY-MM-DD HH:MM:SS

    Возвращает JSON-ответ следующего формата:
    - Приветствие [Доброе утро/день/вечер/ночь] # OK
    - По каждой карте
        - последние 4 цифры карты #
        - общая сумма расходов #
        - кешбэк (1 рубль на каждые 100 рублей) #
    - Топ-5 транзакций по сумме платежа #
    - Курс валют #
    - Стоимость акций из S&P500 #
    """

    greeting = get_greeting(date)  # получить приветствие
    cards, top_transactions = get_cards_info(date)  # получить информацию по картам
    currency_rates = get_exchange_rate()  # получить курс валют
    stock_prices = get_stock_prices()  # получить стоимость акций из S&P500

    full_response = {
        'greeting': greeting,
        'cards': cards,
        'top_transactions': top_transactions,
        'currency_rates': currency_rates,
        'stock_prices': stock_prices
    }

    # запись данных в json-файл
    with open('data/output.json', 'w', encoding='utf-8') as json_file:
        json.dump(full_response, json_file, indent=4, ensure_ascii=False)


def get_greeting(date) -> str:
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    hour = date_obj.hour  # час

    if 6 <= hour < 12:
        return "Доброе утро!"
    elif 12 <= hour < 18:
        return "Добрый день!"
    elif 18 <= hour < 24:
        return "Добрый вечер!"
    else:
        return "Доброй ночи!"


def get_cards_info(date) -> tuple:
    """ Возвращает инфорцию о картах и о топ транзакциях за указаный период """
    # Перевод промежутка отслеживания операций в datetime
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    date_start = date_obj.replace(year=date_obj.year, month=date_obj.month, day=1, hour=0, minute=0, second=0)

    # получение данных и перевод дат в datetime
    operations = read_excel('data/operations.xlsx')
    operations['Дата операции'] = pd.to_datetime(operations['Дата операции'], format='%d.%m.%Y %H:%M:%S')

    # фильтрация по искомому временному промежутку
    date_operations = operations.loc[(operations['Дата операции'] >= date_start)
                                     & (operations['Дата операции'] <= date_obj)]

    # Группировка данных по картам
    grouped_by_cards = date_operations.groupby('Номер карты')

    cards = []
    for card_number, group in grouped_by_cards:
        cards.append({
            'last_digits': card_number[1:],
            'total_spent': sum(group['Сумма операции с округлением']),
            'cashback': sum(group['Бонусы (включая кэшбэк)'])
        })

    top_five_transactions = date_operations.sort_values('Сумма операции с округлением', ascending=False).head()

    top_transactions = []
    for index, row in top_five_transactions.iterrows():
        top_transactions.append({
            'date': row['Дата платежа'],
            'amount': row['Сумма операции с округлением'],
            'category': row['Категория'],
            'description': row['Описание']
        })

    return cards, top_transactions


def read_excel(path_to_file: str):
    """ Возвращает содержимое Excel - файла """
    return pd.read_excel(path_to_file)


def get_exchange_rate() -> list:
    with open('user_settings.json', 'r') as json_file:
        currencies = json.load(json_file)
    currency_rates = []

    api_key = os.getenv('API_KEY_APILAYER')

    payload = {}
    headers = {
        "apikey": api_key
    }

    for currency in currencies['user_currencies']:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount=1"

        response = requests.request("GET", url, headers=headers, data=payload)

        status_code = response.status_code
        result = response.text

        json_to_list = json.loads(result)
        currency_rates.append({
            'currency': currency,
            'rate': json_to_list['info']['rate']
        })
    return currency_rates


def get_stock_prices() -> list:
    with open('user_settings.json', 'r') as json_file:
        user_stocks = json.load(json_file)

    api_key = os.getenv('API_KEY_FINNHUB')
    finnhub_client = finnhub.Client(api_key=api_key)
    stock_prices = []
    for stock in user_stocks['user_stocks']:
        stock_prices.append({
            'stock': stock,
            'price': finnhub_client.quote(stock)['c']
        })

    return stock_prices
