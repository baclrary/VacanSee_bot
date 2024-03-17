from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import CallbackQueryHandler, ContextTypes


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends the main menu with inline buttons."""
    translation = context.user_data["lang"]

    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(translation["scraper_menu"], callback_data="scraper_menu")],
            [InlineKeyboardButton(translation["guide_button"], callback_data="show_guide")],
            [InlineKeyboardButton(translation["configs_button"], callback_data="show_configs")],
            [InlineKeyboardButton(translation["language_button"], callback_data="select_language")],
            [InlineKeyboardButton(translation["contact_button"], callback_data="contact_info")],
        ]
    )

    text = translation["main_menu_title"]

    if update.callback_query:
        query = update.callback_query
        await query.message.edit_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    else:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


main_menu_handler = CallbackQueryHandler(main_menu, pattern="^main_menu$")
