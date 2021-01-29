from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from DB import insert_user
from helpers import set_user_data
from inlinekeyboards import InlineKeyboard
from languages import LANGS


def start_handler_callback(update: Update, context: CallbackContext):
    user_data = context.user_data
    set_user_data(update.effective_user.id, user_data)
    user = user_data['user_data']

    if user:
        if 'user_input_data' not in user_data:

            if user['lang'] == LANGS[0]:
                text = "Robocontest.uz saytining kompilyator botiga xush kelibsiz !\n" \
                       "Dasturlash tillarini ko'rish uchun /languages ni bosing"
            else:
                text = 'Robocontest.uz сайтининг компилятор ботига хуш келибсиз !\n' \
                       'Дастурлаш тилларини кўриш учун /languages ни босинг'

            text = f'\U0001F917    {text}'
            update.message.reply_text(text)
    else:

        text = 'Tilni tanlang\nТилни танланг'
        inline_keyboard = InlineKeyboard('langs_keyboard').get_keyboard()

        update.message.reply_text(text, reply_markup=inline_keyboard)


start_handler = CommandHandler('start', start_handler_callback)
