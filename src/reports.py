import datetime
from typing import Optional

import pandas as pd


# Траты по категориям
def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[str] = datetime.datetime.now()
) -> pd.DataFrame:
    filtered_transactions = []
    return filtered_transactions
