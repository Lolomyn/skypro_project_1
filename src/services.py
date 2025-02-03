import logging
import pandas as pd

from src.reports import report

logger = logging.getLogger("services")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/services.log", "w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


# ПРОСТОЙ ПОИСК
@report("")
def simple_search(key_words: str, operations: pd.DataFrame) -> list:
    """Пользователь передает строку для поиска,
    возвращается JSON-ответ со всеми транзакциями,
    содержащими запрос в описании или категории"""

    try:
        logger.info(f"Операции фильтруются по ключевым данным: {key_words}")
        search_operations = operations.loc[
            (operations["Категория"].str.contains(key_words, case=False, na=False))
            | (operations["Описание"].str.contains(key_words, case=False, na=False))
        ]
        logger.info(f"Возвращено строк: {search_operations.shape[0]}")
        return search_operations
    except ValueError:
        logger.error("Полученный DataFrame некорректен...")
        print("Некорректный DataFrame!")
    except Exception as e:
        logger.error(f"Вызвано исключение {e}")
        print(f"Вызвано исключение {e.__class__.__name__}")
