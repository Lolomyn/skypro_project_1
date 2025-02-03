# ���������� ��� ������� ���������� ��������
by lolomyn

## Description:

���������� ��� ������� ����������, ������� ��������� � Excel-�����. 
���������� ���������� JSON-������ ��� ���-�������, 
��������� Excel-������, � ����� ������������ ������ �������.

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

*main_page* - ���������� ��������� ������, �������� ����

example:
```
- ����������� [������ ����/����/�����/����]
    - �� ������ �����
        - ��������� 4 ����� �����
        - ����� ����� ��������
        - ������ (1 ����� �� ������ 100 ������)
    - ���-5 ���������� �� ����� �������
    - ���� �����
    - ��������� ����� �� S&P500
```
**Output**
```
[
    {
        "greeting": "������ ����!",
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

*get_greeting* - ���������� ����������� � ����������� �� ������� �����

*get_cards_info* - ���������� ���������� � ������ � � ��� ����������� �� ��������� ������

*get_exchange_rate* - ���������� ���� ����� ������������

*get_stock_prices* - ���������� ��������� ����� ������������

*get_data_from_finnhub* - ���������� ����� �� API FINNHUB

*to_python_from_json* - ���������� ���������� JSON �����

*read_excel* - ���������� ���������� Excel - �����

*simple_search* - ������������ �������� ������ ��� ������, ������������ JSON-����� �� ����� ������������,
    ����������� ������ � �������� ��� ���������

example
```
key
{"���������": ["key", "not", "key"], "��������": ["not", "also not", "extra not"]}
```
**OUTPUT**
```
[
    {
        "���������":"key",
        "��������":"not"
    },
    {
        "���������":"key",
        "��������":"extra not"
    }
]
```

*spending_by_category* - ���������� ��������������� DataFrame �� ������� ���������

example
```
"data/operations.xlsx", "������������", "2020-05-20 12:55:32"
```

**OUTPUT**
```
[
    {
        "���� ��������":1589973993000,
        "���� �������":"23.05.2020",
        "����� �����":"*7197",
        "������":"OK",
        "����� ��������":-52.9,
        "������ ��������":"RUB",
        "����� �������":-52.9,
        "������ �������":"RUB",
        "������":null,
        "���������":"������������",
        "MCC":5411.0,
        "��������":"������",
        "������ (������� ������)":1,
        "���������� �� �������������":0,
        "����� �������� � �����������":52.9
    },
    {
        "���� ��������":1589883858000,
        "���� �������":"21.05.2020",
        "����� �����":"*7197",
        "������":"OK",
        "����� ��������":-131.18,
        "������ ��������":"RUB",
        "����� �������":-131.18,
        "������ �������":"RUB",
        "������":null,
        "���������":"������������",
        "MCC":5499.0,
        "��������":"������",
        "������ (������� ������)":2,
        "���������� �� �������������":0,
        "����� �������� � �����������":131.18
    },
    
    ...
    
    {
        "���� ��������":1589835720000,
        "���� �������":"20.05.2020",
        "����� �����":"*7197",
        "������":"OK",
        "����� ��������":-100.0,
        "������ ��������":"RUB",
        "����� �������":-100.0,
        "������ �������":"RUB",
        "������":null,
        "���������":"������������",
        "MCC":5411.0,
        "��������":"�����",
        "������ (������� ������)":2,
        "���������� �� �������������":0,
        "����� �������� � �����������":100.0
    }
]
```

## Tests:
��������� pytest: `poetry add --group dev pytest`

����� `tests` �������� �������� ������:

`test_reports.py` >>> `reports.py`

`test_services.py` >>> `services.py`

`test_utils.py` >>> `utils.py`

`test_views.py` >>> `views.py`

������ `conftest.py` �������� ��������, ������������ ��� ������������.

���������� �������� ������ � ������ `htmlcov` � ������� HTML.

����� ����������� �������� � �������: `pytest --cov`

## Author:
[Mail](vismanmark@yandex.ru) /
[GitHub](https://github.com/Lolomyn)