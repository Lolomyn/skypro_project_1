from dotenv import load_dotenv

from src.reports import report
from src.utils import get_cards_info, get_exchange_rate, get_greeting, get_stock_prices, to_json, to_python_from_json

load_dotenv()


# ГЛАВНАЯ СТРАНИЦА
@report('')
def main_page(date: str) -> list:
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

    try:
        greeting = get_greeting(date)  # получить приветствие
        cards, top_transactions = get_cards_info(date)  # получить информацию по картам
        currency_rates = get_exchange_rate()  # получить курс валют
        stock_prices = get_stock_prices()  # получить стоимость акций из S&P500

        full_response = [
            {
                "greeting": greeting,
                "cards": cards,
                "top_transactions": top_transactions,
                "currency_rates": currency_rates,
                "stock_prices": stock_prices,
            }
        ]

        return full_response
    except ValueError:
        print(f'Дата {date} не соответствует требуемому формату представления! YYYY-MM-DD HH:MM:SS')
    finally:
        print("Конец работы блока main_page.")
        print('________')
