from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
)
from telegram.ext.filters import COMMAND, TEXT

from database.crud import create_config

from .display_configs import display_configs

TITLE, LANG, EXP_YEARS, REGION, SALARY_USD, ENG_LVL, SEARCH_WORDS, REFRESH_TIME_MIN = range(8)


async def send_or_reply(
    update: Update, context: ContextTypes.DEFAULT_TYPE, translation_key: str, reply_markup=None, **kwargs
):
    translation = context.user_data["lang"]
    text = translation[translation_key]
    if update.callback_query:
        query = update.callback_query
        await query.message.edit_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    else:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)


async def start_config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    translations = context.user_data["lang"]

    await update.callback_query.answer()

    if update.callback_query:
        query = update.callback_query
        await query.message.edit_text(translations["config_creation_title"], parse_mode=ParseMode.HTML)
        await query.message.reply_text(translations["config_name_prompt"], parse_mode=ParseMode.HTML)
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=translations["config_creation_title"],
            parse_mode=ParseMode.HTML,
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=translations["config_name_prompt"],
            parse_mode=ParseMode.HTML,
        )
    return TITLE


async def title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["conf_title"] = update.message.text
    await send_or_reply(update, context, "prog_lang_prompt")
    return LANG


async def lang(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["conf_lang"] = update.message.text.lower()
    await send_or_reply(update, context, "years_exp_prompt")
    return EXP_YEARS


async def exp_years(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["conf_exp_years"] = int(update.message.text)
    await send_or_reply(update, context, "specify_region_prompt")
    return REGION


async def region(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["conf_region"] = update.message.text.lower()
    await send_or_reply(update, context, "desired_salary_prompt")
    return SALARY_USD


async def salary_usd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["conf_salary_usd"] = int(update.message.text)
    await send_or_reply(update, context, "english_level_prompt")
    return ENG_LVL


async def eng_lvl(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["conf_eng_lvl"] = update.message.text.lower()
    await send_or_reply(update, context, "search_keywords_prompt")
    return SEARCH_WORDS


async def search_words(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["conf_search_words"] = update.message.text
    await send_or_reply(update, context, "refresh_time_prompt")
    return REFRESH_TIME_MIN


async def refresh_time_min(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["conf_refresh_time_min"] = int(update.message.text)
    config_data = {
        "refresh_time_min": context.user_data["conf_refresh_time_min"],
        "user_id": context.user_data["id"],
        "title": context.user_data["conf_title"],
        "lang": context.user_data["conf_lang"],
        "exp_years": context.user_data["conf_exp_years"],
        "region": context.user_data["conf_region"],
        "salary_usd": context.user_data["conf_salary_usd"],
        "eng_lvl": context.user_data["conf_eng_lvl"],
        "search_words": context.user_data["conf_search_words"],
    }
    await create_config(**config_data)
    await clear_context(update, context)
    await send_or_reply(update, context, "config_saved_success")
    await display_configs(update, context)
    return ConversationHandler.END


async def clear_context(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keys_to_remove = [key for key in context.user_data.keys() if key.startswith("conf_")]
    for key in keys_to_remove:
        context.user_data.pop(key)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await display_configs(update, context)
    return ConversationHandler.END


create_config_conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(start_config, pattern="^create_config$")],
    states={
        TITLE: [MessageHandler(TEXT & ~COMMAND, title)],
        LANG: [MessageHandler(TEXT & ~COMMAND, lang)],
        EXP_YEARS: [MessageHandler(TEXT & ~COMMAND, exp_years)],
        REGION: [MessageHandler(TEXT & ~COMMAND, region)],
        SALARY_USD: [MessageHandler(TEXT & ~COMMAND, salary_usd)],
        ENG_LVL: [MessageHandler(TEXT & ~COMMAND, eng_lvl)],
        SEARCH_WORDS: [MessageHandler(TEXT & ~COMMAND, search_words)],
        REFRESH_TIME_MIN: [MessageHandler(TEXT & ~COMMAND, refresh_time_min)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
