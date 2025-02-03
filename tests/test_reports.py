import json
import logging
from datetime import datetime
from unittest.mock import Mock, mock_open, patch

import pandas as pd

from src.reports import report, spending_by_category

logger = logging.getLogger("utils")


# REPORT
def test_report_with_dict():
    with patch("builtins.open", mock_open()) as mock_file:
        decorator = report("output.json")

        @decorator
        def test_func():
            return {"key": "value"}

        result = test_func()

        assert result == {"key": "value"}

        mock_file.assert_called_once_with("output.json", "w", encoding="utf-8")


def test_report_with_dataframe():
    mock_df = Mock(spec=pd.DataFrame)

    decorator = report("output.json")

    @decorator
    def test_func():
        return mock_df

    result = test_func()

    assert result == mock_df

    mock_df.to_json.assert_called_once_with("output.json", indent=4, orient="records", force_ascii=False)


def test_report_with_default_filename():
    with patch("builtins.open", mock_open()) as mock_file:
        decorator = report(None)

        @decorator
        def test_func():
            return {"key": "value"}

        result = test_func()

        assert result == {"key": "value"}

        mock_file.assert_called_once_with("data/output_test_func.json", "w", encoding="utf-8")


def test_report_with_list():
    with patch("builtins.open", mock_open()) as mock_file:
        decorator = report("output.json")

        @decorator
        def test_func():
            return [1, 2, 3]

        result = test_func()

        assert result == [1, 2, 3]

        mock_file.assert_called_once_with("output.json", "w", encoding="utf-8")


# SPENDING_BY_CATEGORY
def test_spending_by_category_success():
    data = {
        "Дата операции": ["01.01.2023 12:00:00", "15.02.2023 14:00:00", "10.03.2023 16:00:00"],
        "Категория": ["Еда", "Транспорт", "Еда"],
        "Сумма": [100, 200, 150],
    }
    transactions = pd.DataFrame(data)

    test_date = datetime(2023, 3, 10, 16, 0, 0)

    with patch.object(logger, "info") as mock_logger_info:
        result = spending_by_category(transactions, "Еда", test_date)

        expected_data = {
            "Дата операции": ["01.01.2023 12:00:00", "10.03.2023 16:00:00"],
            "Категория": ["Еда", "Еда"],
            "Сумма": [100, 150],
        }
        expected_df = pd.DataFrame(expected_data)
        expected_df["Дата операции"] = pd.to_datetime(expected_df["Дата операции"], format="%d.%m.%Y %H:%M:%S")

        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df.reset_index(drop=True))

        mock_logger_info.assert_any_call(f"Получена дата: {test_date}")
        mock_logger_info.assert_any_call("Просматриваемая категория: Еда")


def test_spending_by_category_with_string_date():

    data = {
        "Дата операции": ["01.01.2023 12:00:00", "15.02.2023 14:00:00", "10.03.2023 16:00:00"],
        "Категория": ["Еда", "Транспорт", "Еда"],
        "Сумма": [100, 200, 150],
    }
    transactions = pd.DataFrame(data)

    with patch.object(logger, "info") as mock_logger_info:
        result = spending_by_category(transactions, "Еда", "2023-03-10 16:00:00")

        expected_data = {
            "Дата операции": ["01.01.2023 12:00:00", "10.03.2023 16:00:00"],
            "Категория": ["Еда", "Еда"],
            "Сумма": [100, 150],
        }
        expected_df = pd.DataFrame(expected_data)
        expected_df["Дата операции"] = pd.to_datetime(expected_df["Дата операции"], format="%d.%m.%Y %H:%M:%S")

        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df.reset_index(drop=True))

        mock_logger_info.assert_any_call("Получена дата: 2023-03-10 16:00:00")
        mock_logger_info.assert_any_call("Просматриваемая категория: Еда")


def test_spending_by_category_invalid_date():
    data = {
        "Дата операции": ["01.01.2023 12:00:00", "15.02.2023 14:00:00", "10.03.2023 16:00:00"],
        "Категория": ["Еда", "Транспорт", "Еда"],
        "Сумма": [100, 200, 150],
    }
    transactions = pd.DataFrame(data)

    with patch("builtins.print") as mock_print:
        result = spending_by_category(transactions, "Еда", "invalid_date")

        assert result is None

        mock_print.assert_called_once_with(
            "Дата invalid_date не соответствует " "требуемому формату представления! YYYY-MM-DD HH:MM:SS"
        )


def test_spending_by_category_not_found():
    # Создаем тестовый DataFrame
    data = {
        "Дата операции": ["01.01.2023 12:00:00", "15.02.2023 14:00:00", "10.03.2023 16:00:00"],
        "Категория": ["Еда", "Транспорт", "Еда"],
        "Сумма": [100, 200, 150],
    }
    transactions = pd.DataFrame(data)

    with patch.object(logger, "info") as mock_logger_info:
        result = spending_by_category(transactions, "Развлечения")

        assert result.empty

        mock_logger_info.assert_any_call("Просматриваемая категория: Развлечения")
