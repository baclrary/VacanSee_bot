from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from ..utils import ensure_user_exists, get_user_translation
from .main_menu import main_menu


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id

    user = await ensure_user_exists(user_id)
    translation = await get_user_translation(user.id)

    context.user_data.update(
        {
            "id": user_id,
            "lang": translation,
        }
    )

    welcome_text = translation.get("welcome_text", "Welcome!")
    await update.message.reply_text(welcome_text)

    await main_menu(update, context)


start_handler = CommandHandler("start", start)
