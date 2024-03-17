from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import CallbackQueryHandler, ContextTypes

from database.crud import get_user_configs


async def display_configs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    translation = context.user_data["lang"]
    configs = await get_user_configs(context.user_data["id"])

    buttons = [[InlineKeyboardButton(translation["create_cfg_button"], callback_data="create_config")]]
    buttons += [
        [InlineKeyboardButton(f"{index + 1}. {config.title}", callback_data=f"get_config_{config.id}")]
        for index, config in enumerate(configs)
    ]

    if configs:
        buttons.append(
            [InlineKeyboardButton(translation["delete_all_cfgs_button"], callback_data="delete_all_configs")]
        )

    buttons.append([InlineKeyboardButton(translation["button_back"], callback_data="main_menu")])

    reply_markup = InlineKeyboardMarkup(buttons)

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=translation["display_user_configs"],
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML,
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=translation["display_user_configs"],
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML,
        )


display_configs_handler = CallbackQueryHandler(display_configs, pattern="^show_configs$")
