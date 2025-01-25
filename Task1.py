from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes
from telegram.ext.filters import TEXT

API_TOKEN = 'Enter your API token here'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! I am your simple AI Assistant. How can I help you today?")

async def process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    response = "I received your message: \"{}\". How can I assist further?".format(user_message)
    await update.message.reply_text(response)

def main():
    app = ApplicationBuilder().token(API_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(TEXT, process))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
