# Приложение для анализа банковских операций
by lolomyn

## Description:

Приложение для анализа транзакций, которые находятся в Excel-файле. 
Приложение генерирует JSON-данные для веб-страниц, 
формирует Excel-отчеты, а также предоставяет другие сервисы.

## Install:

**Ubuntu**

`sudo apt update` - update all packages

- python

`sudo apt install python3` - install python

`python3 -V` - check python version

- git

`sudo apt install git` - install git

`git --version` - check git version

- poetry

`sudo apt install python3-poetry` - install poetry

`poetry --version` - check poetry version

- clone repo

`git clone git@github.com:Lolomyn/skypro_project_1.git`

- install dependencies

`poetry add requests`

- start

`python3 main.py`

**Windows**

`sudo apt update` - update all packages

- python

Download it  [here](https://www.python.org/) and follow instructions

`python --version` - check python version

- git

Download in [here](https://git-scm.com/) and follow instructions

`git --version` - check git version

- poetry

`curl -sSL https://install.python-poetry.org | python -` - install poetry

`poetry --version` - check poetry version

- clone repo

`git clone git@github.com:Lolomyn/skypro_project_1.git`

- install dependencies

`poetry add requests`

- start

`python main.py`

## Functions:

*main_page* - возвращает некоторые данные, принимая дату

example:
```
- Приветствие [Доброе утро/день/вечер/ночь]
    - По каждой карте
        - последние 4 цифры карты
        - общая сумма расходов
        - кешбэк (1 рубль на каждые 100 рублей)
    - Топ-5 транзакций по сумме платежа
    - Курс валют
    - Стоимость акций из S&P500
```
**Output**
```
[
    {
        "greeting": "Добрый день!",
        "cards": [
            {
                "last4": "1234",
                "total_spent": 1000,
                "cashback": 10
            }
        ],
        "top_transactions": [
            {
                "transaction": "example",
                "amount": 500
            }
        ],
        "currency_rates": {
            "USD": 75.0,
            "EUR": 85.0
        },
        "stock_prices": [
            {
                "stock": "AAPL",
                "price": 150.0
            }
        ]
    }
]
```

*get_greeting* - возвращает приветствие в зависимости от времени суток

*get_cards_info* - возвращает информацию о картах и о топ транзакциях за указанный период

*get_exchange_rate* - возвращает курс валют пользователя

*get_stock_prices* - возвращает стоимость акций пользователя

*get_data_from_finnhub* - возвращает ответ от API FINNHUB

*to_python_from_json* - возвращает содержимое JSON файла

*read_excel* - возвращает содержимое Excel - файла

*simple_search* - пользователь передает строку для поиска, возвращается JSON-ответ со всеми транзакциями,
    содержащими запрос в описании или категории

example
```
key
{"Категория": ["key", "not", "key"], "Описание": ["not", "also not", "extra not"]}
```
**OUTPUT**
```
[
    {
        "Категория":"key",
        "Описание":"not"
    },
    {
        "Категория":"key",
        "Описание":"extra not"
    }
]
```

*spending_by_category* - возвращает отфильтрованный DataFrame по искомой категории

example
```
"data/operations.xlsx", "Супермаркеты", "2020-05-20 12:55:32"
```

**OUTPUT**
```
[
    {
        "Дата операции":1589973993000,
        "Дата платежа":"23.05.2020",
        "Номер карты":"*7197",
        "Статус":"OK",
        "Сумма операции":-52.9,
        "Валюта операции":"RUB",
        "Сумма платежа":-52.9,
        "Валюта платежа":"RUB",
        "Кэшбэк":null,
        "Категория":"Супермаркеты",
        "MCC":5411.0,
        "Описание":"Магнит",
        "Бонусы (включая кэшбэк)":1,
        "Округление на инвесткопилку":0,
        "Сумма операции с округлением":52.9
    },
    {
        "Дата операции":1589883858000,
        "Дата платежа":"21.05.2020",
        "Номер карты":"*7197",
        "Статус":"OK",
        "Сумма операции":-131.18,
        "Валюта операции":"RUB",
        "Сумма платежа":-131.18,
        "Валюта платежа":"RUB",
        "Кэшбэк":null,
        "Категория":"Супермаркеты",
        "MCC":5499.0,
        "Описание":"Колхоз",
        "Бонусы (включая кэшбэк)":2,
        "Округление на инвесткопилку":0,
        "Сумма операции с округлением":131.18
    },
    
    ...
    
    {
        "Дата операции":1589835720000,
        "Дата платежа":"20.05.2020",
        "Номер карты":"*7197",
        "Статус":"OK",
        "Сумма операции":-100.0,
        "Валюта операции":"RUB",
        "Сумма платежа":-100.0,
        "Валюта платежа":"RUB",
        "Кэшбэк":null,
        "Категория":"Супермаркеты",
        "MCC":5411.0,
        "Описание":"Дикси",
        "Бонусы (включая кэшбэк)":2,
        "Округление на инвесткопилку":0,
        "Сумма операции с округлением":100.0
    }
]
```

## Tests:
Установка pytest: `poetry add --group dev pytest`

Папка `tests` содержит тестовые модули:

`test_reports.py` >>> `reports.py`

`test_services.py` >>> `services.py`

`test_utils.py` >>> `utils.py`

`test_views.py` >>> `views.py`

Модуль `conftest.py` содержит фикстуры, используемые при тестировании.

Результаты покрытия тестов в пакете `htmlcov` в формате HTML.

Вызов результатов покрытия в консоль: `pytest --cov`

## Author:
[Mail](vismanmark@yandex.ru) /
[GitHub](https://github.com/Lolomyn)