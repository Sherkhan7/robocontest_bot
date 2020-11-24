from telegram.ext import CommandHandler, CallbackContext
from telegram import Update
from helpers import set_user_data


def command_handler_callback(update: Update, context: CallbackContext):
    user_data = context.user_data
    set_user_data(update.effective_user.id, user_data)
    user = user_data['user_data']

    if user:
        pass
    else:
        text = ''


command_handler = CommandHandler(['start, menu'], command_handler_callback)
