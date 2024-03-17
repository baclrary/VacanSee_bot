from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import CallbackQueryHandler, ContextTypes


async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    translation = context.user_data["lang"]
    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(translation["report_bug"], url="https://t.me/the_coffin_is_my_new_room")],
            [InlineKeyboardButton(translation["suggest_idea"], url="https://t.me/the_coffin_is_my_new_room")],
            [InlineKeyboardButton(translation["support_project"], url="https://t.me/the_coffin_is_my_new_room")],
            [InlineKeyboardButton(translation["button_back"], callback_data="main_menu")],
        ]
    )
    await update.callback_query.edit_message_text(
        text=translation["contact_text"], reply_markup=reply_markup, parse_mode=ParseMode.HTML
    )


contact_handler = CallbackQueryHandler(contact, pattern="^contact_info$")
