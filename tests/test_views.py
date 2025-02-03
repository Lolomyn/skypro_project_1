from unittest.mock import patch

from src.views import main_page


def test_main_page_success(fixture_main_page_data):
    with patch("src.views.get_greeting", return_value="Добрый день!"), patch(
        "src.views.get_cards_info",
        return_value=(
            [{"last4": "1234", "total_spent": 1000, "cashback": 10}],
            [{"transaction": "example", "amount": 500}],
        ),
    ), patch("src.views.get_exchange_rate", return_value={"USD": 75.0, "EUR": 85.0}), patch(
        "src.views.get_stock_prices", return_value=[{"stock": "AAPL", "price": 150.0}]
    ):

        result = main_page("")
        expected_result = fixture_main_page_data
        assert result == expected_result
