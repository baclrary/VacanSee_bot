import logging

from telegram.ext import Application

from settings import TOKEN

from .handlers import all_handlers

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def run_bot() -> None:
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()
    [application.add_handler(handler) for handler in all_handlers]
    application.run_polling()


def main() -> None:
    run_bot()


if __name__ == "__main__":
    main()
