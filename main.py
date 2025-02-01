import json

from src.views import get_info

if __name__ == "__main__":
    get_info("2020-05-20 12:55:32")  # YYYY-MM-DD HH:MM:SS
    with open("data/output.json", "r", encoding="utf-8") as json_file:
        operations = json.load(json_file)

    # print(operations)
