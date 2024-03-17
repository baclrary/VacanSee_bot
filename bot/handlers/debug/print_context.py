from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes


async def print_context(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.edit_text(f"{context.user_data}")


print_context_handler = CallbackQueryHandler(print_context, pattern="^print_context$")
