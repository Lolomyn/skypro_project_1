import pandas as pd
import pytest
from unittest.mock import patch, Mock
import logging

from src.utils import read_excel

# Импортируем функцию, которую будем тестировать

# Настройка логгера для тестов
logger = logging.getLogger('utils')  # Замените `your_module` на имя вашего модуля


# Тест на успешное чтение файла
def test_read_excel_success():
    # Мокируем pd.read_excel, чтобы он возвращал фиктивный DataFrame
    with patch('pandas.read_excel') as mock_read_excel:
        mock_read_excel.return_value = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

        # Вызываем функцию
        result = read_excel('dummy_path.xlsx')

        # Проверяем, что функция вернула ожидаемый DataFrame
        assert isinstance(result, pd.DataFrame)
        assert not result.empty
        mock_read_excel.assert_called_once_with('dummy_path.xlsx')


# Тест на случай, если файл не найден
def test_read_excel_file_not_found():
    # Мокируем pd.read_excel, чтобы он вызывал FileNotFoundError
    with patch('pandas.read_excel') as mock_read_excel:
        mock_read_excel.side_effect = FileNotFoundError

        # Вызываем функцию
        result = read_excel('nonexistent_path.xlsx')

        # Проверяем, что функция вернула None
        assert result is None
        mock_read_excel.assert_called_once_with('nonexistent_path.xlsx')


# Тест на логирование
def test_read_excel_logging():
    # Мокируем pd.read_excel и logger.info
    with patch('pandas.read_excel') as mock_read_excel, patch.object(logger, 'info') as mock_logger_info:
        mock_read_excel.return_value = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

        # Вызываем функцию
        read_excel('dummy_path.xlsx')

        # Проверяем, что логгер был вызван с правильным сообщением
        mock_logger_info.assert_called_once_with("Возвращение содержимого эксель файла dummy_path.xlsx")


# Параметризованный тест для проверки различных сценариев
@pytest.mark.parametrize("file_path, expected_output, exception", [
    ('valid_path.xlsx', pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]}), None),
    ('nonexistent_path.xlsx', None, FileNotFoundError),
])
def test_read_excel_parametrized(file_path, expected_output, exception):
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