from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from database.crud import update_user

from ..utils import get_user_translation


async def select_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Allows the user to select a language."""
    translation = context.user_data["lang"]

    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("English 🇬🇧", callback_data="set_lang_eng")],
            [InlineKeyboardButton("Українська 🇺🇦", callback_data="set_lang_ukr")],
            [InlineKeyboardButton(translation["button_back"], callback_data="main_menu")],
        ]
    )

    if update.callback_query:
        query = update.callback_query
        await query.edit_message_text(text=translation["choose_language"], reply_markup=reply_markup)
    else:
        await update.message.reply_text(text=translation["choose_language"], reply_markup=reply_markup)


async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = context.user_data["id"]
    language = update.callback_query.data.split("_")[-1]
    await update_user(user_id=user_id, lang=language)

    context.user_data["lang"] = await get_user_translation(user_id)
    translation = context.user_data["lang"]

    await select_language(update, context)
    await update.callback_query.answer(text=translation.get("language_set", "Your language has been set!"))


set_language_handler = CallbackQueryHandler(set_language, pattern="^set_lang_")
language_selection_handler = CallbackQueryHandler(select_language, pattern="^select_language$")
