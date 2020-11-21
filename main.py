from telegram.ext import Updater
from config.config import TOKEN
from handlers import (message_handler)


def main():
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(message_handler)

    # updater.start_polling()
    # updater.idle()

    updater.start_webhook(listen='127.0.0.1', port=5002, url_path=TOKEN)
    updater.bot.set_webhook(url='https://cardel.ml/' + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
