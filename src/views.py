import datetime
import json

import pandas as pd
import requests


def get_info(date: str) -> str:
    """Принимает дату в формате: YYYY-MM-DD HH:MM:SS

    Возвращает JSON-ответ следующего формата:
    - Приветствие [Доброе утро/день/вечер/ночь]
    - По каждой карте
        - последние 4 цифры карты
        - общая сумма расходов
        - кешбэк (1 рубль на каждые 100 рублей)
    - Топ-5 транзакций по сумме платежа
    - Курс валют
    - Стоимость акций из S&P500
    """

    greeting = get_greeting(date)
    cards = get_cards_info(date)
    top_transactions = get_top_transactions()
    currency_rates = get_exchange_rate()
    stock_prices = get_stock_prices()

    full_response = {
        'greeting': greeting,
        'cards': cards,
        'top_transactions': top_transactions,
        'currency_rates': currency_rates,
        'stock_prices': stock_prices
    }
    full_response_to_json = json.dumps(full_response, indent=4)

    return full_response_to_json


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


def get_cards_info(date) -> list:
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    date_start = date_obj.replace(year=date_obj.year, month=date_obj.month, day=1, hour=0, minute=0, second=0)

    # date_start_str = date_start.strftime("%d.%m.%Y %H:%M:%S")
    # date_now = date_obj.strftime("%d.%m.%Y %H:%M:%S")

    operations = pd.read_excel('data/operations.xlsx')
    operations['Дата операции'] = pd.to_datetime(operations['Дата операции'], format='%d.%m.%Y %H:%M:%S')
    date_operations = operations.loc[(operations['Дата операции'] > date_start)
                                     & (operations['Дата операции'] < date_obj)]
    cards = operations['Номер карты'].unique()  # список всех карт
    print(date_operations['Дата операции'])
    return []


def get_top_transactions() -> list:
    return []


def get_exchange_rate() -> list:
    return []


def get_stock_prices() -> list:
    return []
