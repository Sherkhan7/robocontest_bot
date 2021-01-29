from telegram.ext import Updater, PicklePersistence
from config import TOKEN
from handlers import *


def main():
    my_persistence = PicklePersistence('my_pickle', store_chat_data=False, single_file=False)

    updater = Updater(TOKEN, persistence=my_persistence)

    # updater.dispatcher.add_handler(message_handler)
    updater.dispatcher.add_handler(conversation_handler)
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(inline_keyboards_handler)

    # updater.start_polling()
    # updater.idle()

    updater.start_webhook(listen='127.0.0.1', port=5003, url_path=TOKEN)
    updater.bot.set_webhook(url='https://cardel.ml/' + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
