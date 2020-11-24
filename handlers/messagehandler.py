from telegram.ext import MessageHandler, Filters, CallbackContext
from telegram import Update
from inlinekeyboards import InlineKeyboard
from helpers import set_user_data
from languages import LANGS


def message_handler_callback(update: Update, context: CallbackContext):
    user_data = context.user_data
    set_user_data(update.effective_user.id, user_data)
    user = user_data['user_data']

    if user:

        inline_keyboard = InlineKeyboard('program_langs_keyboard').get_keyboard()

        if user['lang'] == LANGS[0]:
            text = 'Dasturlash tili tanlang'
        else:
            text = 'Дастурлаш тили танланг'

        update.message.reply_text(text, reply_markup=inline_keyboard)
    else:
        text = 'Tilni tanlang\nТилни танланг'
        inline_keyboard = InlineKeyboard('langs_keyboard').get_keyboard()

        update.message.reply_text(text, reply_markup=inline_keyboard, quote=True)


message_handler = MessageHandler(filters=Filters.text & (~ Filters.command), callback=message_handler_callback)
