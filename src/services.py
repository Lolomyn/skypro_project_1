from src.utils import read_excel, to_json, to_python_from_json


# ПРОСТОЙ ПОИСК
def simple_search(key_words: str) -> dict:
    """ Пользователь передает строку для поиска,
    возвращается JSON-ответ со всеми транзакциями,
    содержащими запрос в описании или категории."""

    operations = read_excel("data/operations.xlsx")

    search_operations = operations.loc[(operations['Категория'].str.contains(key_words, case=False, na=False)) |
                                       (operations['Описание'].str.contains(key_words, case=False, na=False))]
    search_result = search_operations.to_dict(orient='records')
    to_json('data/simple_search.json', search_result)
    response = to_python_from_json('data/simple_search.json')
    return response
