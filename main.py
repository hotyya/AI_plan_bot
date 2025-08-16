import logging
import utils.logger.build_logger
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from utils.creds import TELEGRAM_TOKEN
from model import get_answer
from parse import update_plans

logger = logging.getLogger('bot_logger')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"User {update.effective_user.id} started the bot.")
    await update.message.reply_text("Привет! Я бот по магистратурам AI. Задай свой вопрос.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    logger.info(f"Received message: {user_input}")
    answer = get_answer(user_input)
    await update.message.reply_text(answer)

def main():
    update_plans()
    
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot is starting...")
    app.run_polling()

if __name__ == "__main__":
    main()