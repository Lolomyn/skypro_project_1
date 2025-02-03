import json
import logging
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
import pytest

from src.utils import (
    get_cards_info,
    get_data_from_finnhub,
    get_exchange_rate,
    get_greeting,
    get_stock_prices,
    read_excel,
    to_python_from_json,
)

logger = logging.getLogger("utils")


# READ_EXCEL
def test_read_excel_valid():
    with patch("pandas.read_excel") as mock_read_excel:
        mock_read_excel.return_value = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})

        result = read_excel("path.xlsx")

        assert isinstance(result, pd.DataFrame)
        assert not result.empty
        mock_read_excel.assert_called_once_with("path.xlsx")


def test_read_excel_no_file():
    with patch("pandas.read_excel") as mock_read_excel:
        mock_read_excel.side_effect = FileNotFoundError

        result = read_excel("no_exist_path.xlsx")

        assert result is None
        mock_read_excel.assert_called_once_with("no_exist_path.xlsx")


def test_read_excel_logging():
    with patch("pandas.read_excel") as mock_read_excel, patch.object(logger, "info") as mock_logger_info:
        mock_read_excel.return_value = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})

        read_excel("path.xlsx")

        mock_logger_info.assert_called_once_with("Возвращение содержимого эксель файла path.xlsx")


@pytest.mark.parametrize(
    "file_path, expected_output, exception",
    [
        ("valid_path.xlsx", pd.DataFrame({"col1": [1, 2], "col2": [3, 4]}), None),
        ("no_exist_path.xlsx", None, FileNotFoundError),
    ],
)
def test_read_excel(file_path, expected_output, exception):
    with patch("pandas.read_excel") as mock_read_excel:
        if exception:
            mock_read_excel.side_effect = exception
        else:
            mock_read_excel.return_value = expected_output

        result = read_excel(file_path)

        if exception:
            assert result is None
        else:
            assert result.equals(expected_output)
        mock_read_excel.assert_called_once_with(file_path)


# TO_PYTHON_FROM_JSON
def test_to_python_from_json_valid():
    mock_json_data = json.dumps({"key": "value"})

    with patch("builtins.open", mock_open(read_data=mock_json_data)), patch.object(logger, "info") as mock_logger_info:
        result = to_python_from_json("path.json")
        assert result == {"key": "value"}
        mock_logger_info.assert_called_once_with("Получение данных из path.json")


def test_to_python_from_json_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError), patch.object(logger, "error") as mock_logger_error:
        with pytest.raises(Exception, match="Файл не найден!"):
            to_python_from_json("no_exist_path.json")

        mock_logger_error.assert_called_once_with("Попытка открыть файл no_exist_path.json. Не успешно.")


def test_to_python_from_json_invalid_json():
    with patch("builtins.open", mock_open(read_data="invalid json")), patch.object(
        logger, "error"
    ) as mock_logger_error:
        with pytest.raises(Exception, match="Файл не найден!"):
            to_python_from_json("invalid_path.json")

        mock_logger_error.assert_called_once_with("Попытка открыть файл invalid_path.json. Не успешно.")


def test_to_python_from_json_other_error():
    with patch("builtins.open", side_effect=PermissionError), patch.object(logger, "error") as mock_logger_error:
        with pytest.raises(Exception, match="Файл не найден!"):
            to_python_from_json("restricted_path.json")

        mock_logger_error.assert_called_once_with("Попытка открыть файл restricted_path.json. Не успешно.")


# GET_DATA_FROM_FINNHUB
def test_get_data_from_finnhub_success():
    with patch("os.getenv", return_value="test_api_key"), patch("finnhub.Client") as mock_finnhub_client:
        result = get_data_from_finnhub()

        mock_finnhub_client.assert_called_once_with(api_key="test_api_key")
        assert result == mock_finnhub_client.return_value


def test_get_data_from_finnhub_client_initialization_failure():
    with patch("os.getenv", return_value="test_api_key"), patch(
        "finnhub.Client", side_effect=Exception("Initialization error")
    ):
        with pytest.raises(Exception) as exc_info:
            get_data_from_finnhub()
        assert str(exc_info.value) == "Initialization error"


# GET_GREETING
def test_get_greeting_morning():
    with patch.object(logger, "info") as mock_logger_info:
        result = get_greeting("2023-10-05 08:00:00")

        assert result == "Доброе утро!"

        mock_logger_info.assert_any_call("Получена дата: 2023-10-05 08:00:00")
        mock_logger_info.assert_any_call("Получен час для вывода приветствия: 8")
        mock_logger_info.assert_any_call("Возвращенное приветствие: Доброе утро!")


def test_get_greeting_afternoon():
    with patch.object(logger, "info") as mock_logger_info:
        result = get_greeting("2023-10-05 13:00:00")

        assert result == "Добрый день!"

        mock_logger_info.assert_any_call("Получена дата: 2023-10-05 13:00:00")
        mock_logger_info.assert_any_call("Получен час для вывода приветствия: 13")
        mock_logger_info.assert_any_call("Возвращенное приветствие: Добрый день!")


def test_get_greeting_evening():
    with patch.object(logger, "info") as mock_logger_info:
        result = get_greeting("2023-10-05 19:00:00")

        assert result == "Добрый вечер!"

        mock_logger_info.assert_any_call("Получена дата: 2023-10-05 19:00:00")
        mock_logger_info.assert_any_call("Получен час для вывода приветствия: 19")
        mock_logger_info.assert_any_call("Возвращенное приветствие: Добрый вечер!")


def test_get_greeting_night():
    with patch.object(logger, "info") as mock_logger_info:
        result = get_greeting("2023-10-05 02:00:00")

        assert result == "Доброй ночи!"

        mock_logger_info.assert_any_call("Получена дата: 2023-10-05 02:00:00")
        mock_logger_info.assert_any_call("Получен час для вывода приветствия: 2")
        mock_logger_info.assert_any_call("Возвращенное приветствие: Доброй ночи!")


def test_get_greeting_invalid_date():
    with patch.object(logger, "error") as mock_logger_error, patch("builtins.print") as mock_print:

        result = get_greeting("invalid_date")

        assert result is None
        mock_logger_error.assert_called_once_with("Дата invalid_date не валидна.")
        mock_print.assert_called_once_with(
            "Дата invalid_date не соответствует требуемому формату представления!" "YYYY-MM-DD HH:MM:SS"
        )


# GET_CARDS_INFO
def test_get_cards_info_success():
    with patch("src.utils.read_excel") as mock_read_excel, patch.object(logger, "info") as mock_logger_info:
        mock_data = pd.DataFrame(
            {
                "Дата операции": ["01.01.2023 10:00:00", "15.01.2023 12:00:00", "20.01.2023 14:00:00"],
                "Номер карты": ["*1234", "*5678", "*1234"],
                "Сумма операции с округлением": [100.0, 200.0, 300.0],
                "Бонусы (включая кэшбэк)": [10.0, 20.0, 30.0],
                "Дата платежа": ["01.01.2023", "15.01.2023", "20.01.2023"],
                "Категория": ["Продукты", "Одежда", "Электроника"],
                "Описание": ["Покупка продуктов", "Покупка одежды", "Покупка электроники"],
            }
        )
        mock_read_excel.return_value = mock_data

        date = "2023-01-31 23:59:59"

        cards, top_transactions = get_cards_info(date)

        assert len(cards) == 2
        assert cards[0] == {"last_digits": "1234", "total_spent": 400.0, "cashback": 40.0}
        assert cards[1] == {"last_digits": "5678", "total_spent": 200.0, "cashback": 20.0}

        assert len(top_transactions) == 3
        assert top_transactions[0] == {
            "date": "20.01.2023",
            "amount": 300.0,
            "category": "Электроника",
            "description": "Покупка электроники",
        }
        assert top_transactions[1] == {
            "date": "15.01.2023",
            "amount": 200.0,
            "category": "Одежда",
            "description": "Покупка одежды",
        }
        assert top_transactions[2] == {
            "date": "01.01.2023",
            "amount": 100.0,
            "category": "Продукты",
            "description": "Покупка продуктов",
        }

        mock_logger_info.assert_any_call("Диапазон фильтрации: 2023-01-01 00:00:00 - 2023-01-31 23:59:59")
        mock_logger_info.assert_any_call("Получен отфильтрованный DataFrame")
        mock_logger_info.assert_any_call("Данные успешно сгруппированы по картам")
        mock_logger_info.assert_any_call("Получен список словарей карт и операций по ним")
        mock_logger_info.assert_any_call("Получен DataFrame с пятью самыми дорогими операциями")
        mock_logger_info.assert_any_call("Получен список словарей топ транзакций и их информации")


def test_get_cards_info_invalid_date_format():
    with patch("src.utils.read_excel") as mock_read_excel, patch.object(logger, "error") as mock_logger_error:
        mock_read_excel.return_value = pd.DataFrame()

        date = "invalid_date_format"
        get_cards_info(date)

        mock_logger_error.assert_called_once_with("Вызвано исключение ValueError")


def test_get_cards_info_empty_data():
    with patch("src.utils.read_excel") as mock_read_excel, patch.object(
        logger, "info"
    ) as mock_logger_info, patch.object(logger, "error") as mock_logger_error:
        mock_read_excel.return_value = pd.DataFrame()

        date = "2023-01-31 23:59:59"

        cards, top_transactions = get_cards_info(date)

        assert cards == []
        assert top_transactions == []

        mock_logger_info.assert_any_call("Диапазон фильтрации: 2023-01-01 00:00:00 - 2023-01-31 23:59:59")
        mock_logger_error.assert_any_call("Переданный файл пуст, возвращаются пустые списки")


def test_get_cards_info_missing_columns():
    with patch("src.utils.read_excel") as mock_read_excel, patch.object(logger, "error") as mock_logger_error:
        mock_data = pd.DataFrame(
            {
                "Дата операции": ["01.01.2023 10:00:00"],
                "Номер карты": ["*1234"],
                "Сумма операции с округлением": [100.0],
                # Отсутствует колонка "Бонусы (включая кэшбэк)"
            }
        )
        mock_read_excel.return_value = mock_data

        date = "2023-01-31 23:59:59"

        get_cards_info(date)
        mock_logger_error.assert_called_once_with("Вызвано исключение KeyError")


# GET_EXCHANGE_RATE
def test_get_exchange_rate_success():
    with patch("src.utils.os.getenv") as mock_getenv, patch("src.utils.requests.request") as mock_request, patch(
        "builtins.open", new_callable=mock_open, read_data=json.dumps({"user_currencies": ["USD", "EUR"]})
    ), patch.object(logger, "info") as mock_logger_info:
        mock_getenv.return_value = "test_api_key"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = json.dumps({"info": {"rate": 75.0}, "success": True})
        mock_request.return_value = mock_response

        result = get_exchange_rate()

        assert result == [{"currency": "USD", "rate": 75.0}, {"currency": "EUR", "rate": 75.0}]
        mock_logger_info.assert_any_call("Обработана валюта: USD")
        mock_logger_info.assert_any_call("Обработана валюта: EUR")


def test_get_exchange_rate_status_code_429():
    with patch("src.utils.os.getenv") as mock_getenv, patch("src.utils.requests.request") as mock_request, patch(
        "builtins.open", new_callable=mock_open, read_data=json.dumps({"user_currencies": ["USD", "EUR"]})
    ), patch.object(logger, "error") as mock_logger_error:
        mock_getenv.return_value = "test_api_key"
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.text = "Rate limit exceeded"
        mock_request.return_value = mock_response

        result = get_exchange_rate()

        assert result == []
        mock_logger_error.assert_any_call("Количество запросов на API превышено")


def test_get_exchange_rate_empty_json():
    with patch("src.utils.os.getenv") as mock_getenv, patch(
        "builtins.open", new_callable=mock_open, read_data=json.dumps({})
    ):
        mock_getenv.return_value = "test_api_key"

        result = get_exchange_rate()

        assert result == []


# GET_STOCK_PRICES
def test_get_stock_prices_empty_json():
    with patch("src.utils.to_python_from_json") as mock_to_python_from_json, patch(
        "src.utils.get_data_from_finnhub"
    ) as mock_get_data_from_finnhub:
        mock_to_python_from_json.return_value = {}

        mock_finnhub_client = MagicMock()
        mock_finnhub_client.quote.side_effect = [{"c": 150.0}, {"c": 300.0}]
        mock_get_data_from_finnhub.return_value = mock_finnhub_client

        result = get_stock_prices()
        assert result == []
