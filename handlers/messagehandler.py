from telegram.ext import MessageHandler, Filters, CallbackContext
from telegram import Update


def message_handler_callback(update: Update, context: CallbackContext):
    update.message.reply_text(f'\U0001F642	Salom {update.effective_user.first_name} !')


message_handler = MessageHandler(filters=Filters.text, callback=message_handler_callback)
