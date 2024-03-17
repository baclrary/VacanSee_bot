from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from database.crud import delete_all_user_configs

from .display_configs import display_configs


async def ask_delete_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Asks the user to confirm deletion of all configurations."""
    translation = context.user_data["lang"]

    await update.callback_query.edit_message_text(
        text=context.user_data["lang"]["cfgs_delete_confirm"],
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(f"{translation['yes']} ✅", callback_data="confirm_delete_all_configs")],
                [InlineKeyboardButton(f"{translation['no']} ❌", callback_data="cancel_delete_all_configs")],
            ]
        ),
    )


async def confirm_delete_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Deletes all user configurations after confirmation."""
    await delete_all_user_configs(update.callback_query.from_user.id)
    await display_configs(update, context)


async def cancel_delete_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancels the deletion of all configurations."""
    await display_configs(update, context)


ask_delete_all_configs_confirmation_handler = CallbackQueryHandler(
    ask_delete_confirmation, pattern="^delete_all_configs$"
)
confirm_delete_all_configs_handler = CallbackQueryHandler(confirm_delete_all, pattern="^confirm_delete_all_configs$")
cancel_delete_all_configs_handler = CallbackQueryHandler(cancel_delete_all, pattern="^cancel_delete_all_configs$")
