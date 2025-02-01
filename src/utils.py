import datetime
import json
import os

import finnhub
import pandas
import pandas as pd
import requests
from dotenv import load_dotenv


def get_greeting(date: str) -> str:
    """���������� ����������� � ����������� �� ������� �����"""
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    hour = date_obj.hour  # ���

    if 6 <= hour < 12:
        return "������ ����!"
    elif 12 <= hour < 18:
        return "������ ����!"
    elif 18 <= hour < 24:
        return "������ �����!"
    else:
        return "������ ����!"


def get_cards_info(date: str) -> tuple:
    """���������� �������� � ������ � � ��� ����������� �� �������� ������"""
    # ������� ���������� ������������ �������� � datetime
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    date_start = date_obj.replace(year=date_obj.year, month=date_obj.month, day=1, hour=0, minute=0, second=0)

    # ��������� ������ � ������� ��� � datetime
    operations = read_excel("data/operations.xlsx")
    operations["���� ��������"] = pd.to_datetime(operations["���� ��������"], format="%d.%m.%Y %H:%M:%S")

    # ���������� �� �������� ���������� ����������
    date_operations = operations.loc[
        (operations["���� ��������"] >= date_start) & (operations["���� ��������"] <= date_obj)
    ]

    # ����������� ������ �� ������
    grouped_by_cards = date_operations.groupby("����� �����")

    cards = []
    for card_number, group in grouped_by_cards:
        cards.append(
            {
                "last_digits": card_number[1:],
                "total_spent": sum(group["����� �������� � �����������"]),
                "cashback": sum(group["������ (������� ������)"]),
            }
        )

    top_five_transactions = date_operations.sort_values("����� �������� � �����������", ascending=False).head()

    top_transactions = []
    for index, row in top_five_transactions.iterrows():
        top_transactions.append(
            {
                "date": row["���� �������"],
                "amount": row["����� �������� � �����������"],
                "category": row["���������"],
                "description": row["��������"],
            }
        )

    return cards, top_transactions


def read_excel(path_to_file: str) -> pandas.DataFrame:
    """���������� ���������� Excel - �����"""
    return pd.read_excel(path_to_file)


def get_exchange_rate() -> list:
    """���������� ���� ����� ������������"""
    with open("user_settings.json", "r") as json_file:
        currencies = json.load(json_file)
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
    return currency_rates


def get_stock_prices() -> list:
    """���������� ��������� ����� ������������"""
    with open("user_settings.json", "r") as json_file:
        user_stocks = json.load(json_file)

    stock_prices: list = []

    api_key = os.getenv("API_KEY_FINNHUB")
    finnhub_client = finnhub.Client(api_key=api_key)

    for stock in user_stocks['user_stocks']:
        stock_prices.append({
            'stock': stock,
            'price': finnhub_client.quote(stock)['c']
        })

    return stock_prices
