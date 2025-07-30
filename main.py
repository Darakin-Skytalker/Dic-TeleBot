import os
import menu as m
import handlers as h
from telegram.ext import (ApplicationBuilder, MessageHandler, CommandHandler,
                          filters, CallbackQueryHandler)

# Define your bot token
# BOT_TOKEN = "your token value here"
BOT_TOKEN = os.environ.get("BOT_TOKEN")


# Build the app
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Add handlers
app.add_handler(CommandHandler("start", h.start))
app.add_handler(CommandHandler("pronunciation", h.send_pdf))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, m.receive_word))
app.add_handler(CallbackQueryHandler(m.button_handler))


# Run the bot
app.run_polling()