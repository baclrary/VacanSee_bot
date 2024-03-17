from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import CallbackQueryHandler, ContextTypes

from database.crud import get_user_configs

running_tasks = {}


async def scraper_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = context.user_data["id"]
    translation = context.user_data["lang"]
    configs = await get_user_configs(user_id)

    keyboard_buttons = []

    if configs and not running_tasks.get(user_id):
        keyboard_buttons.append([InlineKeyboardButton(translation["run_scraper_button"], callback_data="run_scraper")])

    if running_tasks.get(user_id):
        keyboard_buttons.append(
            [InlineKeyboardButton(translation["stop_scraper_button"], callback_data="stop_scraping")]
        )

    keyboard_buttons.append([InlineKeyboardButton(translation["button_back"], callback_data="main_menu")])

    if not configs:
        text = translation["no_config_found_text"]
    else:
        text = (
            translation["scraper_is_working"] if running_tasks.get(user_id) else translation["scraper_is_not_working"]
        )

    if update.callback_query:
        await update.callback_query.message.edit_text(
            text, reply_markup=InlineKeyboardMarkup(keyboard_buttons), parse_mode=ParseMode.HTML
        )
    else:
        await update.message.reply_text(
            text, reply_markup=InlineKeyboardMarkup(keyboard_buttons), parse_mode=ParseMode.HTML
        )


scraper_menu_handler = CallbackQueryHandler(scraper_menu, pattern="^scraper_menu$")
