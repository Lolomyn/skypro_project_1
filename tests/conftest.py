import pytest


@pytest.fixture()
def fixture_main_page_data():
    return [
        {
            "greeting": "Добрый день!",
            "cards": [{"last4": "1234", "total_spent": 1000, "cashback": 10}],
            "top_transactions": [{"transaction": "example", "amount": 500}],
            "currency_rates": {"USD": 75.0, "EUR": 85.0},
            "stock_prices": [{"stock": "AAPL", "price": 150.0}],
        }
    ]
