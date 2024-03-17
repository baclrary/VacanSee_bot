from .run_scraper import run_scraper_handler, stop_scraping_handler
from .scraper_menu import scraper_menu_handler

all_scraper_handlers = [
    run_scraper_handler,
    stop_scraping_handler,
    scraper_menu_handler,
]
