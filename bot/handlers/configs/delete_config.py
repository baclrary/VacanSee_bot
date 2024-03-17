from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from database.crud import delete_config

from .display_configs import display_configs


async def ask_delete_config_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Asks the user to confirm deletion of a specific configuration."""
    translation = context.user_data["lang"]
    config_id = update.callback_query.data.split("_")[-1]

    await update.callback_query.edit_message_text(
        text=translation["cfg_delete_confirm"],
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(f"{translation['yes']} ✅", callback_data=f"confirm_delete_config_{config_id}")],
                [InlineKeyboardButton(f"{translation['no']} ❌", callback_data="cancel_delete_config")],
            ]
        ),
    )


async def confirm_delete_config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Deletes a specific configuration after confirmation."""
    config_id = update.callback_query.data.split("_")[-1]
    await delete_config(config_id)
    await display_configs(update, context)


async def cancel_delete_config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancels the deletion of a configuration."""
    await display_configs(update, context)


ask_delete_config_confirmation_handler = CallbackQueryHandler(
    ask_delete_config_confirmation, pattern="^ask_delete_config_"
)
confirm_delete_config_handler = CallbackQueryHandler(confirm_delete_config, pattern="^confirm_delete_config_")
cancel_delete_config_handler = CallbackQueryHandler(cancel_delete_config, pattern="^cancel_delete_config$")
