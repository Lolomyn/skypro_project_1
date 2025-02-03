import datetime
import json
import logging
import os

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
    try:
        logger.info(f"Получена дата: {date}")
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        hour = date_obj.hour  # час
        logger.info(f"Получен час для вывода приветствия: {hour}")

        if 6 <= hour < 12:
            logger.info("Возвращенное приветствие: Доброе утро!")
            return "Доброе утро!"
        elif 12 <= hour < 18:
            logger.info("Возвращенное приветствие: Добрый день!")
            return "Добрый день!"
        elif 18 <= hour < 24:
            logger.info("Возвращенное приветствие: Добрый вечер!")
            return "Добрый вечер!"
        else:
            logger.info("Возвращенное приветствие: Доброй ночи!")
            return "Доброй ночи!"
    except ValueError:
        logger.error(f"Дата {date} не валидна.")
        print(f"Дата {date} не соответствует требуемому формату представления! YYYY-MM-DD HH:MM:SS")


def get_cards_info(date: str) -> tuple:
    """Возвращает информацию о картах и о топ транзакциях за указанный период"""
    try:
        # перевод промежутка отслеживания операций в datetime
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        date_start = date_obj.replace(year=date_obj.year, month=date_obj.month, day=1, hour=0, minute=0, second=0)
        logger.info(f"Диапазон фильтрации: {date_start} - {date_obj}")

        # получение данных и перевод дат в datetime
        operations = read_excel("data/operations.xlsx")
        if operations.empty:
            logger.error("Переданный файл пуст, возвращаются пустые списки")
            return [], []

        operations["Дата операции"] = pd.to_datetime(operations["Дата операции"], format="%d.%m.%Y %H:%M:%S")

        # фильтрация по искомому временному промежутку
        date_operations = operations.loc[
            (operations["Дата операции"] >= date_start) & (operations["Дата операции"] <= date_obj)
        ]
        logger.info("Получен отфильтрованный DataFrame")

        # группировка данных по картам
        grouped_by_cards = date_operations.groupby("Номер карты")
        logger.info("Данные успешно сгруппированы по картам")

        cards = []
        for card_number, group in grouped_by_cards:
            cards.append(
                {
                    "last_digits": card_number[1:],
                    "total_spent": sum(group["Сумма операции с округлением"]),
                    "cashback": sum(group["Бонусы (включая кэшбэк)"]),
                }
            )
        logger.info("Получен список словарей карт и операций по ним")

        top_five_transactions = date_operations.sort_values("Сумма операции с округлением", ascending=False).head()
        logger.info("Получен DataFrame с пятью самыми дорогими операциями")

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
        logger.info("Получен список словарей топ транзакций и их информации")
        logger.info("Возвращены списки словарей")
        return cards, top_transactions
    except ValueError:
        print("Переданные данные некорректны!")
        logger.error("Вызвано исключение ValueError")
    except KeyError:
        print("Содержимое считываемого файла невалидно!")
        logger.error("Вызвано исключение KeyError")


def get_exchange_rate() -> list:
    """Возвращает курс валют пользователя"""
    with open("user_settings.json", "r") as json_file:
        currencies = json.load(json_file)
    logger.info(f"Запись данных из {json_file}")
    currency_rates: list = []

    api_key = os.getenv("API_KEY_APILAYER")

    payload: dict = {}
    headers = {"apikey": api_key}

    if currencies:
        for currency in currencies["user_currencies"]:
            url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount=1"

            response = requests.request("GET", url, headers=headers, data=payload)

            status_code = response.status_code
            result = response.text
            if status_code == 200:
                json_to_list = json.loads(result)
                currency_rates.append({"currency": currency, "rate": json_to_list["info"]["rate"]})
                logger.info(f"Обработана валюта: {currency}")
            else:
                print(result)
                logger.error("Количество запросов на API превышено")
    else:
        return currency_rates
    logger.info("Возвращен пустой список")
    return currency_rates


def get_stock_prices() -> list:
    """Возвращает стоимость акций пользователя"""
    try:
        user_stocks: dict = to_python_from_json("user_settings.json")
        finnhub_client = get_data_from_finnhub()
        stock_prices: list = []
        if user_stocks:
            for stock in user_stocks["user_stocks"]:
                stock_prices.append({"stock": stock, "price": finnhub_client.quote(stock)["c"]})
                logger.info(f"Обработана акция: {stock} по цене {finnhub_client.quote(stock)['c']}")

        return stock_prices
    except Exception as e:
        logger.error(f"Вызвано исключение {e.__class__.__name__}")
        print(f"Exception: {e.__class__.__name__}")
        return []


def get_data_from_finnhub() -> finnhub.client.Client:
    """Возвращает ответ от API"""
    api_key = os.getenv("API_KEY_FINNHUB")
    finnhub_client = finnhub.Client(api_key=api_key)
    logger.info("Получение ответа от finnhub")
    return finnhub_client


def to_python_from_json(path: str) -> dict | list:
    """Возвращает содержимое JSON файла"""
    try:
        with open(path, "r", encoding="utf-8") as json_file:
            logger.info(f"Получение данных из {path}")
            return json.load(json_file)
    except Exception:
        logger.error(f"Попытка открыть файл {path}. Не успешно.")
        raise Exception("Файл не найден!")


def read_excel(path_to_file: str) -> pandas.DataFrame:
    """Возвращает содержимое Excel - файла"""
    try:
        logger.info(f"Возвращение содержимого эксель файла {path_to_file}")
        return pd.read_excel(path_to_file)
    except FileNotFoundError:
        logger.error(f"Попытка открыть файл {path_to_file}. Не успешно.")
        print(f"Файла по адресу {path_to_file} не существует!")
