import json
import logging
from datetime import datetime
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

from src.utils import to_json, to_python_from_json

logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/utils.log", "w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def report(filename):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if filename:
                if isinstance(result, pd.DataFrame):
                    result.to_json(filename, indent=4, orient='records', force_ascii=False)
                else:
                    with open(filename, 'w', encoding='utf-8') as file:
                        json.dump(result, file, ensure_ascii=False, indent=4)
            else:
                if isinstance(result, pd.DataFrame):
                    result.to_json(f'data/output_{func.__name__}.json', indent=4, orient='records', force_ascii=False)
                else:
                    with open(f'data/output_{func.__name__}.json', 'w', encoding='utf-8') as file:
                        json.dump(result, file, ensure_ascii=False, indent=4)

        return wrapper
    return decorator


# ТРАТЫ ПО КАТЕГОРИЯМ
@report('')
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = datetime.now()) \
        -> pd.DataFrame:
    logger.info(f"Получена дата: {date}")
    try:
        if isinstance(date, datetime):
            date_start = date - relativedelta(months=3)
            date_obj = date
        else:
            date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            date_start = date_obj - relativedelta(months=3)
        logger.info(f"Получена диапазон фильтрации: {date_start} - {date_obj}")

        transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")

        # фильтрация по искомому временному промежутку
        date_operations = transactions.loc[
            (transactions["Дата операции"] >= date_start) & (transactions["Дата операции"] <= date_obj)
        ]
        logger.info(f"Просматриваемая категория: {category}")

        filtered_df = date_operations[date_operations['Категория'] == category]
        return filtered_df
    except ValueError:
        print(f'Дата {date} не соответствует требуемому формату представления! YYYY-MM-DD HH:MM:SS')
    finally:
        print('Конец работы блока spending_by_category.')
        print('________')
