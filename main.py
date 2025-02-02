from src.reports import spending_by_category
from src.services import simple_search
from src.utils import read_excel
from src.views import main_page

if __name__ == "__main__":
    main_page_response = main_page("2020-12-20 00:00:00")  # YYYY-MM-DD HH:MM:SS
    #
    # simple_search_response = simple_search('аптека')
    #
    # spending_by_category_response = spending_by_category(read_excel("data/operations.xlsx"),
    #                                                      "Супермаркеты", "2020-05-20 12:55:32")
    #
    #
