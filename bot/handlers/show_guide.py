from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import CallbackQueryHandler, ContextTypes


async def show_guide(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    translation = context.user_data["lang"]
    guide_text = translation["guide_text"]
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(translation["button_back"], callback_data="main_menu")]])

    await update.callback_query.edit_message_text(text=guide_text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


show_guide_handler = CallbackQueryHandler(show_guide, pattern="^show_guide$")
