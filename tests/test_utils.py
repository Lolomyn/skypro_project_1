import json
import os

import pandas as pd
import pytest
from unittest.mock import patch, Mock, mock_open
import logging

from src.utils import read_excel, get_stock_prices, to_python_from_json, get_data_from_finnhub

logger = logging.getLogger('utils')


def test_read_excel_valid():
    with patch('pandas.read_excel') as mock_read_excel:
        mock_read_excel.return_value = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

        result = read_excel('path.xlsx')

        assert isinstance(result, pd.DataFrame)
        assert not result.empty
        mock_read_excel.assert_called_once_with('path.xlsx')


def test_read_excel_no_file():
    with patch('pandas.read_excel') as mock_read_excel:
        mock_read_excel.side_effect = FileNotFoundError

        result = read_excel('no_exist_path.xlsx')

        assert result is None
        mock_read_excel.assert_called_once_with('no_exist_path.xlsx')


def test_read_excel_logging():
    with patch('pandas.read_excel') as mock_read_excel, patch.object(logger, 'info') as mock_logger_info:
        mock_read_excel.return_value = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

        read_excel('path.xlsx')

        mock_logger_info.assert_called_once_with("Возвращение содержимого эксель файла path.xlsx")


@pytest.mark.parametrize("file_path, expected_output, exception", [
    ('valid_path.xlsx', pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]}), None),
    ('no_exist_path.xlsx', None, FileNotFoundError),
])
def test_read_excel(file_path, expected_output, exception):
    with patch('pandas.read_excel') as mock_read_excel:
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


def test_to_python_from_json_valid():
    mock_json_data = json.dumps({"key": "value"})

    with patch("builtins.open", mock_open(read_data=mock_json_data)), patch.object(logger, 'info') as mock_logger_info:
        result = to_python_from_json("path.json")

        assert result == {"key": "value"}

        mock_logger_info.assert_called_once_with("Получение данных из path.json")


def test_to_python_from_json_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError), patch.object(logger, 'error') as mock_logger_error:
        with pytest.raises(Exception, match="Файл не найден!"):
            to_python_from_json("no_exist_path.json")

        mock_logger_error.assert_called_once_with("Попытка открыть файл no_exist_path.json. Не успешно.")


def test_to_python_from_json_invalid_json():
    with patch("builtins.open", mock_open(read_data="invalid json")), patch.object(logger, 'error') as mock_logger_error:
        with pytest.raises(Exception, match="Файл не найден!"):
            to_python_from_json("invalid_path.json")

        mock_logger_error.assert_called_once_with("Попытка открыть файл invalid_path.json. Не успешно.")


def test_to_python_from_json_other_error():
    with patch("builtins.open", side_effect=PermissionError), patch.object(logger, 'error') as mock_logger_error:
        with pytest.raises(Exception, match="Файл не найден!"):
            to_python_from_json("restricted_path.json")

        mock_logger_error.assert_called_once_with("Попытка открыть файл restricted_path.json. Не успешно.")


def test_get_data_from_finnhub_success():
    """
    Тест проверяет, что функция корректно создает и возвращает объект finnhub.Client,
    если переменная окружения API_KEY_FINNHUB установлена.
    """
    # Arrange
    with patch("os.getenv", return_value="test_api_key"), \
         patch("finnhub.Client") as mock_finnhub_client:
        # Act
        result = get_data_from_finnhub()

        # Assert
        mock_finnhub_client.assert_called_once_with(api_key="test_api_key")
        assert result == mock_finnhub_client.return_value


def test_get_data_from_finnhub_client_initialization_failure():
    with patch("os.getenv", return_value="test_api_key"), \
         patch("finnhub.Client", side_effect=Exception("Initialization error")):

        with pytest.raises(Exception) as exc_info:
            get_data_from_finnhub()
        assert str(exc_info.value) == "Initialization error"
