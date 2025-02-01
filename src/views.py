from dotenv import load_dotenv

from src.utils import get_greeting, get_cards_info, get_exchange_rate, get_stock_prices, to_json, to_python_from_json

load_dotenv()


# ГЛАВНАЯ СТРАНИЦА
def main_page(date: str) -> dict:
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

    greeting = get_greeting(date)  # получить приветствие
    cards, top_transactions = get_cards_info(date)  # получить информацию по картам
    currency_rates = get_exchange_rate()  # получить курс валют
    stock_prices = get_stock_prices()  # получить стоимость акций из S&P500

    full_response = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }

    to_json('data/main_page.json', full_response)
    response = to_python_from_json('data/main_page.json')
    return response


