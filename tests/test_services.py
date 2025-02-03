import logging
from unittest.mock import patch

import pandas as pd

from src.services import simple_search

logger = logging.getLogger("services")


def test_simple_search_success():
    with patch.object(logger, "info") as mock_logger_info:
        data = {"Категория": ["key", "not", "key"], "Описание": ["not", "also not", "extra not"]}
        df = pd.DataFrame(data)

        expected_data = {"Категория": ["key", "key"], "Описание": ["not", "extra not"]}
        expected_df = pd.DataFrame(expected_data)

        result = simple_search("key", df)

        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_df.reset_index(drop=True))

        mock_logger_info.assert_any_call("Операции фильтруются по ключевым данным: key")
        mock_logger_info.assert_any_call("Возвращено строк: 2")
