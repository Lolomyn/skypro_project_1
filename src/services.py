from src.reports import report
from src.utils import read_excel


# ПРОСТОЙ ПОИСК
@report('')
def simple_search(key_words: str) -> list:
    """Пользователь передает строку для поиска,
    возвращается JSON-ответ со всеми транзакциями,
    содержащими запрос в описании или категории."""

    try:
        operations = read_excel("data/operations.xlsx")

        search_operations = operations.loc[
            (operations["Категория"].str.contains(key_words, case=False, na=False))
            | (operations["Описание"].str.contains(key_words, case=False, na=False))
        ]

        return search_operations
    except Exception as e:
        print(f"Вызвано исключение {e.__class__.__name__}")
