import asyncio

from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import CallbackQueryHandler, ContextTypes

from database.crud import get_user_configs

from .scraper_menu import running_tasks
from .scrapers import DouScrapper


async def notify_new_vacancies(scraper, bot: Bot, chat_id: int):
    base_msg = "<b>🚨 New {qty} found:</b>"
    qty = "vacancies (" + str(len(scraper.new_vacancies)) + ")" if len(scraper.new_vacancies) > 1 else "vacancy"
    message = [base_msg.format(qty=qty)]

    for vacancy in scraper.new_vacancies[:5]:
        message.append(
            f"\n\n<b>Title:</b> {vacancy['title']}"
            f"\n<b>Company:</b> {vacancy['company_name']}"
            f"\n<b>Location:</b> {vacancy['location']}"
            f"\n<a href='{vacancy['url']}'>View Vacancy</a>"
        )

    if len(scraper.new_vacancies) > 5:
        message.append("\n\n<i>Go to your config to see remaining</i>")

    await bot.send_message(chat_id=chat_id, text="".join(message), parse_mode=ParseMode.HTML)


async def run_scrapers(configs, bot: Bot, chat_id: int):
    async def run_and_notify(config):
        scraper = DouScrapper(config)
        await scraper.start()
        if scraper.new_vacancies:
            await notify_new_vacancies(scraper, bot, chat_id)

    await asyncio.gather(*(run_and_notify(config) for config in configs))


async def setting_task(config, bot: Bot, chat_id: int):
    while True:
        await run_scrapers([config], bot, chat_id)
        await asyncio.sleep(config.refresh_time_min * 60)


async def manage_scraping(update: Update, context: ContextTypes.DEFAULT_TYPE, start: bool):
    chat_id = update.effective_chat.id
    user_id = context.user_data["id"]
    translation = context.user_data["lang"]
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(translation["button_back"], callback_data="main_menu")]])
    text_key = "scrapper_successfuly_ran" if start else "scrapper_successfuly_stopped"

    if start:
        configs = await get_user_configs(user_id)
        running_tasks[user_id] = [asyncio.create_task(setting_task(config, context.bot, chat_id)) for config in configs]
    else:
        if tasks := running_tasks.pop(user_id, None):
            for task in tasks:
                task.cancel()

    text_method = update.callback_query.message.edit_text if update.callback_query else update.message.reply_text
    await text_method(translation[text_key], reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def run_scraper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await manage_scraping(update, context, start=True)


async def stop_scraping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await manage_scraping(update, context, start=False)


run_scraper_handler = CallbackQueryHandler(run_scraper, pattern="^run_scraper$")
stop_scraping_handler = CallbackQueryHandler(stop_scraping, pattern="^stop_scraping$")
