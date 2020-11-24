from telegram.ext import ConversationHandler, CallbackQueryHandler, CallbackContext, CommandHandler, MessageHandler, \
    Filters
from telegram import Update, ParseMode
from helpers import set_user_data
from inlinekeyboards import InlineKeyboard
from languages import LANGS
from helpers import wrap_tags
from DB import insert_attempt
import requests

CHOOSE_PROGRAM_LANG = 'choose_program_lang'
CODE = 'code'
INPUT = 'input'
CONFIRMATION = 'confirmation'


def command_callback(updata: Update, context: CallbackContext):
    user_data = context.user_data
    set_user_data(updata.effective_user.id, user_data)
    user = user_data['user_data']

    if user:
        inline_keyboard = InlineKeyboard('program_langs_keyboard').get_keyboard()

        if user['lang'] == LANGS[0]:
            text = 'Dasturlash tilini tanlang'
        else:
            text = 'Дастурлаш тилини танланг'

        text = f'{text} :'
        message = updata.message.reply_text(text, reply_markup=inline_keyboard)

        state = CHOOSE_PROGRAM_LANG

        user_data['user_input_data'] = dict()
        user_data['user_input_data']['status'] = state
        user_data['user_input_data']['user_tg_id'] = user['tg_id']
        user_data['user_input_data']['message_id'] = message.message_id

        return state


def program_lang_callback(updata: Update, context: CallbackContext):
    user_data = context.user_data
    user = user_data['user_data']

    callback_query = updata.callback_query
    data = callback_query.data

    if user['lang'] == LANGS[0]:
        edit_text = 'Tanlangan til'
        reply_text = 'Menga kodlaringizni yuboring\nBekor qilish uchun /cancel ni yuboring'
    else:
        edit_text = 'Танланган тил'
        reply_text = 'Менга кодларингизни юборинг\nБекор қилиш учун /cancel ни юборинг'
    edit_text = wrap_tags(f'{edit_text} : {data}')
    reply_text = f'\U0001F4DD   {reply_text}:'

    callback_query.answer()
    callback_query.edit_message_text(edit_text, parse_mode=ParseMode.HTML)
    callback_query.message.reply_text(reply_text)

    state = CODE
    user_data['user_input_data']['lang'] = data
    user_data['user_input_data']['status'] = state

    return state


def code_callback(updata: Update, context: CallbackContext):
    # with open('jsons/update.json', 'w') as update_file:
    #     update_file.write(updata.to_json())
    user_data = context.user_data
    user = user_data['user_data']

    code = updata.message.text.strip()
    user_data['user_input_data']['code'] = code

    if user['lang'] == LANGS[0]:
        text = "Kirivchi ma'lumotlarni yuboring (input)"
    else:
        text = "Киривчи маълумотларни юборинг (input)"

    updata.message.reply_text(text)

    state = INPUT
    user_data['user_input_data']['status'] = state

    return state


def input_callback(updata: Update, context: CallbackContext):
    user_data = context.user_data
    user = user_data['user_data']

    input = updata.message.text.strip()
    user_data['user_input_data']['input'] = input

    inline_keyboard = InlineKeyboard('confirm_keyboard', lang=user['lang']).get_keyboard()

    if user['lang'] == LANGS[0]:
        input_text = "Kirivchi ma'lumotlar(input)"
        code_text = 'Kod'
    else:
        input_text = "Киривчи маълумотлар (input)"
        code_text = 'Код'

    code = user_data["user_input_data"]["code"]
    code = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    text = f'{code_text}:\n{code}\n\n' \
           f'{input_text}:\n{user_data["user_input_data"]["input"]}'

    text = f'<code>{text}</code>'
    message = updata.message.reply_text(text, reply_markup=inline_keyboard, parse_mode=ParseMode.HTML)

    state = CONFIRMATION
    user_data['user_input_data']['status'] = state
    user_data['user_input_data']['message_id'] = message.message_id

    return state


def confirm_callback(updata: Update, context: CallbackContext):
    user_data = context.user_data
    user = user_data['user_data']

    callback_query = updata.callback_query
    data = callback_query.data

    if data == 'confirm':
        callback_query.edit_message_reply_markup(None)
        value = send_request_to_api(user_data['user_input_data'])

        if value:

            if user['lang'] == LANGS[0]:
                text = 'Qabul qilindi\nTez orada javobni yetkazaman'
            else:
                text = 'Қабул қилинди\nТез орада жавобни етказаман'

            text += ' \U0001F609'

        else:
            text = 'ERROR'

    callback_query.message.reply_text(text)

    del user_data['user_input_data']
    return ConversationHandler.END


def send_request_to_api(attempt_data):
    url = 'https://robocontest.uz/api/contests/upcoming'
    url_2 = 'https://robocontest.uz/api/ide/run'

    headers = {
        'X-Authorization': '4WUHNAXkag685PwBOpnKymUHD9QAKZp9XZp1gh0kI0BDrhcdsvkZtO3oDy8xRwcd'
    }

    params = {
        'lang': attempt_data['lang'],
        'code': attempt_data['code'],
        'input': attempt_data['input'],
        'callback_url': 'https://cardel.ml/api'
    }
    r = requests.post(url_2, headers=headers, data=params)
    r = r.json()

    print(r)

    if 'id' in r:
        attempt_data['attempt_id'] = r['id']
        attempt_data['status'] = 'waiting'

        value = insert_attempt(attempt_data)

        if value:
            return value
    else:
        print('id not fount in response')


def cancel_callback(updata: Update, context: CallbackContext):
    user_data = context.user_data
    user = user_data['user_data']

    if user['lang'] == LANGS[0]:
        text = 'Bekor qilindi'
    else:
        text = 'Бекор қилинди'

    text = f'\U0001F615 {text} !'

    if user_data['user_input_data']['status'] == CHOOSE_PROGRAM_LANG:
        context.bot.edit_message_text(text, user['tg_id'], user_data['user_input_data']['message_id'])

    else:
        updata.message.reply_text(text)

    del user_data['user_input_data']
    return ConversationHandler.END


conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('menu', command_callback)],
    states={
        CHOOSE_PROGRAM_LANG: [
            CallbackQueryHandler(program_lang_callback,
                                 pattern='^(python2|python3|java|js|pascal|cpp|csharp|php|go|kotlin|PascalABC.NET|)$')],
        CODE: [MessageHandler(Filters.text & (~ Filters.command), code_callback)],
        INPUT: [MessageHandler(Filters.text & (~ Filters.command), input_callback)],
        CONFIRMATION: [CallbackQueryHandler(confirm_callback, pattern='^confirm$')]
    },
    fallbacks=[CommandHandler('cancel', cancel_callback)],
    persistent=True,
    name='code_conversation'
)
