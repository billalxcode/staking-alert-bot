from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

TELEGRAM_TOKEN = "7134780818:AAHwhRSnQ6GOOiL55GpZ2dJccWEfNTE_mnA"
GROUP_ID = -4112324237

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print ("Ping")
    effective_chat_id = update.effective_chat.id
    effective_message = update.effective_message
    effective_user    = update.effective_user
    print (effective_chat_id)

    text = f"""
Pong!!!!

ChatID: {effective_chat_id}
MessageID: {effective_message.id}
UserID: {effective_user.id}
Username: @{effective_user.username}
    """
    await context.bot.send_message(
        effective_chat_id,
        text=text
    )

async def block(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_chat_id = update.effective_chat.id
    print (effective_chat_id)

    text = f"""
Sorry you can't communicate with this bot, please join the Official Community group to get more info
    """
    await context.bot.send_message(
        effective_chat_id,
        text=text
    )

def main():
    print ("Building app")
    application = Application.builder().token(TELEGRAM_TOKEN).read_timeout(30).write_timeout(30).build()
    application.add_handler(
        CommandHandler("ping", ping)
    )
    # application.add_handler(
    #     MessageHandler(filters.TEXT & ~filters.COMMAND, block)
    # )
    application.run_polling()

if __name__ == "__main__":
    main()