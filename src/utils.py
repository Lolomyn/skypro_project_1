import datetime
import json
import os
import logging
import finnhub
import pandas
import pandas as pd
import requests

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/utils.log", "w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_greeting(date: str) -> str:
    """Возвращает приветствие в зависимости от времени суток"""
    logger.info(f"Получена дата: {date}")
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    hour = date_obj.hour  # час
    logger.info(f"Получена час для вывода приветствия: {hour}")

    if 6 <= hour < 12:
        logger.info(f"Возвращенное приветствие: Доброе утро!")
        return "Доброе утро!"
    elif 12 <= hour < 18:
        logger.info(f"Возвращенное приветствие: Добрый день!")
        return "Добрый день!"
    elif 18 <= hour < 24:
        logger.info(f"Возвращенное приветствие: Добрый вечер!")
        return "Добрый вечер!"
    else:
        logger.info(f"Возвращенное приветствие: Доброй ночи!")
        return "Доброй ночи!"


def get_cards_info(date: str) -> tuple:
    """Возвращает инфорцию о картах и о топ транзакциях за указаный период"""
    # перевод промежутка отслеживания операций в datetime
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    date_start = date_obj.replace(year=date_obj.year, month=date_obj.month, day=1, hour=0, minute=0, second=0)
    logger.info(f"Диапазон фильтрации: {date_start} - {date_obj}")

    # получение данных и перевод дат в datetime
    operations = read_excel("data/operations.xlsx")
    operations["Дата операции"] = pd.to_datetime(operations["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    # фильтрация по искомому временному промежутку
    date_operations = operations.loc[
        (operations["Дата операции"] >= date_start) & (operations["Дата операции"] <= date_obj)
        ]
    logger.info(f"Получен отфильтрованный DataFrame")

    # Группировка данных по картам
    grouped_by_cards = date_operations.groupby("Номер карты")
    logger.info(f"Данные успешно сгруппированы по картам")

    cards = []
    for card_number, group in grouped_by_cards:
        cards.append(
            {
                "last_digits": card_number[1:],
                "total_spent": sum(group["Сумма операции с округлением"]),
                "cashback": sum(group["Бонусы (включая кэшбэк)"]),
            }
        )
    logger.info(f"Получен список словарей карт и операций по ним")

    top_five_transactions = date_operations.sort_values("Сумма операции с округлением", ascending=False).head()
    logger.info(f"Получен DataFrame с пятью самыми дорогими операциями")

    top_transactions = []
    for index, row in top_five_transactions.iterrows():
        top_transactions.append(
            {
                "date": row["Дата платежа"],
                "amount": row["Сумма операции с округлением"],
                "category": row["Категория"],
                "description": row["Описание"],
            }
        )
    logger.info(f"Получен список словарей топ транзакций и их информации")
    logger.info(f"Возвращены списки словарей")
    return cards, top_transactions


def read_excel(path_to_file: str) -> pandas.DataFrame:
    """Возвращает содержимое Excel - файла"""
    logger.info(f"Возвращение содержимого эксель файла {path_to_file}")
    return pd.read_excel(path_to_file)


def get_exchange_rate() -> list:
    """Возвращает курс валют пользователя"""
    with open("user_settings.json", "r") as json_file:
        currencies = json.load(json_file)
    logger.info(f"Запись данных из {json_file}")
    currency_rates: list = []

    api_key = os.getenv("API_KEY_APILAYER")

    payload: dict = {}
    headers = {"apikey": api_key}

    for currency in currencies['user_currencies']:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount=1"

        response = requests.request("GET", url, headers=headers, data=payload)

        # status_code = response.status_code
        result = response.text

        json_to_list = json.loads(result)
        currency_rates.append({
            'currency': currency,
            'rate': json_to_list['info']['rate']
        })
        logger.info(f"Обработана валюта: {currency}")
    return currency_rates


def get_stock_prices() -> list:
    """Возвращает стоимость акций пользователя"""
    with open("user_settings.json", "r") as json_file:
        user_stocks = json.load(json_file)
    logger.info(f"Запись данных из {json_file}")

    stock_prices: list = []

    api_key = os.getenv("API_KEY_FINNHUB")
    finnhub_client = finnhub.Client(api_key=api_key)

    for stock in user_stocks['user_stocks']:
        stock_prices.append({
            'stock': stock,
            'price': finnhub_client.quote(stock)['c']
        })
        logger.info(f"Обработана акция: {stock} по цене {finnhub_client.quote(stock)['c']}")

    return stock_prices


def to_json(path_to_file, data):
    """ Записывает данные в JSON файл """
    with open(path_to_file, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

    logger.info(f"Запись данных в {path_to_file}")


def to_python_from_json(path):
    with open(path, "r", encoding="utf-8") as json_file:
        logger.info(f"Получение данных из {path}")
        return json.load(json_file)
