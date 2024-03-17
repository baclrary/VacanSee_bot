from .configs import all_configs_handlers
from .debug import all_debug_handlers
from .main_menu import main_menu_handler
from .scraper import all_scraper_handlers
from .select_language import language_selection_handler, set_language_handler
from .show_contact import contact_handler
from .show_guide import show_guide_handler
from .start import start_handler

all_handlers = (
    [
        main_menu_handler,
        language_selection_handler,
        set_language_handler,
        contact_handler,
        start_handler,
        show_guide_handler,
    ]
    + all_configs_handlers
    + all_scraper_handlers
    # + all_debug_handlers
)
