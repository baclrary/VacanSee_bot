from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import CallbackQueryHandler, ContextTypes

from database.crud import get_config as get_user_config


async def format_vacancies_text(vacancies, translation):
    if not vacancies:
        return f"\n{translation['cfg_no_vacancies_found']}"
    return f"\n{translation['cfg_vacancies']}\n" + "\n".join(
        f"{idx + 1}. <b>{vac.title}</b> at {vac.company_name} ({vac.location}), <a href='{vac.url}'>Link</a>"
        for idx, vac in enumerate(vacancies)
    )


async def format_config_text(config, vacancies_text, translation):
    config_details = [
        f"<b>{translation['cfg_name']}:</b> {config.title}",
        f"<b>{translation['cfg_language']}:</b> {config.lang}",
        f"<b>{translation['cfg_experience']}:</b> {config.exp_years} {translation['year']}.",
        f"<b>{translation['cfg_region']}:</b> {config.region}",
        f"<b>{translation['cfg_salary']}:</b> {config.salary_usd}$",
        f"<b>{translation['cfg_english']}:</b> {config.eng_lvl}",
        f"<b>{translation['cfg_search_words']}:</b> {config.search_words}",
        f"<b>{translation['cfg_refresh']}:</b> {config.refresh_time_min} {translation['min']}.",
        f"<b>{translation['cfg_active']}:</b> {'✅' if config.is_active else '❌'}",
        f"<b>{translation['cfg_date']}:</b> {config.updated_on.strftime('%Y-%m-%d %H:%M:%S')}",
        vacancies_text,
    ]
    return "\n".join(config_details)


async def get_config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    translation = context.user_data["lang"]
    config_id = (
        int(update.callback_query.data.split("_")[-1]) if update.callback_query else context.user_data["c_config"].id
    )
    config = context.user_data["c_config"] = await get_user_config(config_id)
    configs_text = await format_config_text(
        config, await format_vacancies_text(config.vacancies, context.user_data["lang"]), context.user_data["lang"]
    )

    reply_markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(f"{translation['cfg_edit_button']}", callback_data=f"edit_config_{config.id}")],
            [
                InlineKeyboardButton(
                    f"{translation['cfg_delete_button']}", callback_data=f"ask_delete_config_{config.id}"
                )
            ],
            [InlineKeyboardButton(f"{translation['button_back']}", callback_data="show_configs")],
        ]
    )
    text = f"{translation['cfg_details_title']}\n\n{configs_text}"
    if update.callback_query:
        await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup, parse_mode=ParseMode.HTML
        )


get_config_handler = CallbackQueryHandler(get_config, pattern="^get_config_\d+$")
