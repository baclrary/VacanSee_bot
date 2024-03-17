from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from database.crud import update_config

from .get_config import get_config

EDIT_CONFIG, EDIT_CONFIG_VALUE = range(2)


async def create_keyboard(config, translation):
    """Creates an inline keyboard for editing config options."""
    options = [
        (f"{translation['cfg_name']}", "title"),
        (f"{translation['cfg_language']}", "lang"),
        (f"{translation['cfg_experience']}", "exp_years"),
        (f"{translation['cfg_region']}", "region"),
        (f"{translation['cfg_salary']}", "salary_usd"),
        (f"{translation['cfg_english']}", "eng_lvl"),
        (f"{translation['cfg_search_words']}", "search_words"),
        (f"{translation['cfg_refresh']}", "refresh_time_min"),
        (
            f"{translation['cfg_deactivate']}" if config.is_active else f"{translation['cfg_activate']}",
            "toggle_active_status",
        ),
        (f"{translation['button_back']}", "cancel"),
    ]
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton(text, callback_data=f"{action}_{config.id}")] for text, action in options]
    )


async def start_edit_config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer() if update.callback_query else None
    reply_markup = await create_keyboard(context.user_data["c_config"], context.user_data["lang"])

    message_text = context.user_data["lang"]["cfg_edit_what_change"]
    if update.callback_query:
        await update.callback_query.edit_message_text(text=message_text, reply_markup=reply_markup)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message_text, reply_markup=reply_markup)

    return EDIT_CONFIG


async def edit_field(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles editing of individual config fields."""
    translation = context.user_data["lang"]

    await update.callback_query.answer()
    action, _ = update.callback_query.data.rsplit("_", 1)
    context.user_data["edit_field"] = action

    if action == "cancel":
        context.user_data.pop("edit_field")
        return await cancel(update, context)

    if action == "toggle_active_status":
        return await toggle_active_status(update, context)

    await update.callback_query.edit_message_text(
        text=f"{translation['cfg_edit_enter_new_value']} {action.replace('_', ' ')}.\n{translation['cfg_edit_you_may_cancel']}."
    )
    return EDIT_CONFIG_VALUE


async def update_config_value(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Updates a config value based on user input."""
    field_name = context.user_data["edit_field"]
    new_value = (
        int(update.message.text)
        if field_name in ["exp_years", "salary_usd", "refresh_time_min"]
        else update.message.text
    )
    await update_config(config_id=context.user_data["c_config"].id, **{field_name: new_value})
    await update.message.reply_text(f"{field_name.replace('_', ' ').capitalize()} updated successfully.")
    return await start_edit_config(update, context)


async def toggle_active_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Toggles the active status of a config."""
    translation = context.user_data["lang"]

    config = context.user_data["c_config"]
    new_status = not config.is_active

    context.user_data["c_config"] = await update_config(config_id=config.id, is_active=new_status)
    await update.callback_query.edit_message_text(
        text=f"{translation['cfg_edit_status_upd']}: {translation['cfg_active'] if new_status else translation['cfg_inactivate']}."
    )
    return await start_edit_config(update, context)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancels the edit operation and returns to the initial config state."""
    if update.callback_query:
        await update.callback_query.answer()
        await get_config(update, context)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Configuration edit cancelled.")
        await get_config(update, context)
    return ConversationHandler.END


edit_config_conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(start_edit_config, pattern="^edit_config_\d+$")],
    states={
        EDIT_CONFIG: [CallbackQueryHandler(edit_field)],
        EDIT_CONFIG_VALUE: [MessageHandler(filters.TEXT & ~filters.COMMAND, update_config_value)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
