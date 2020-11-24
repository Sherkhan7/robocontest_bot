from telegram.ext import CallbackQueryHandler, CallbackContext
from telegram import Update
from helpers import set_user_data
from DB import insert_user
from languages import LANGS


def inline_keyboards_handler_callback(update: Update, context: CallbackContext):
    user_data = context.user_data

    callback_query = update.callback_query

    if not user_data['user_data']:
        user_data['user_data'] = dict()
        user_data['user_data']['tg_id'] = update.effective_user.id
        user_data['user_data']['lang'] = callback_query.data

        insert_user(user_data['user_data'])
        del user_data['user_data']

    set_user_data(update.effective_user.id, user_data)
    user = user_data['user_data']

    if callback_query.data == LANGS[0]:
        edit_text = "Til: O'zbekcha (lotin)"
    else:
        edit_text = 'Тил: Ўзбекча (кирил)'

    callback_query.edit_message_text(edit_text)

    if user['lang']:
        text = "Robocontest.uz saytining kompilyator botiga xush kelibsiz !\n" \
               "Dasturlash tillarini ko'rish uchun /menu ni bosing"
    else:
        text = 'Robocontest.uz сайтининг компилятор ботига хуш келибсиз !\n' \
               'Дастурлаш тилларини кўриш учун /menu ни босинг'

    text = f'\U0001F917    {text}'

    callback_query.message.reply_text(text)


inline_keyboards_handler = CallbackQueryHandler(inline_keyboards_handler_callback, pattern='^(uz|cy)$')
