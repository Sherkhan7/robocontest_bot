from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from inlinekeyboards.programminglangs import program_langs


class InlineKeyboard(object):
    def __init__(self, keyb_type, lang=None):

        self.__type = keyb_type
        self.__lang = lang
        self.__keyboard = self.__create_inline_keyboard(self.__type, self.__lang)

    def __create_inline_keyboard(self, keyb_type, lang):

        if keyb_type == 'langs_keyboard':

            return self.__get_langs_keyboard()

        elif keyb_type == 'program_langs_keyboard':

            return self.__program_langs__keyboard()

        elif keyb_type == 'confirm_keyboard':

            return self.__confirm__keyboard(lang)

    @staticmethod
    def __get_langs_keyboard():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("\U0001F1FA\U0001F1FF O'zbekcha (lotin)", callback_data='uz')],
            [InlineKeyboardButton("\U0001F1FA\U0001F1FF Ўзбекча (кирил)", callback_data='cy')],
        ])

    @staticmethod
    def __program_langs__keyboard():
        length = len(program_langs)
        if length % 2 == 0:
            keyboard = [
                [
                    InlineKeyboardButton(program_langs[i]['fullname'], callback_data=program_langs[i]['name']),

                    InlineKeyboardButton(program_langs[i + 1]['fullname'], callback_data=program_langs[i + 1]['name'])
                ]

                for i in range(0, length, 2)
            ]

        else:
            keyboard = [
                [
                    InlineKeyboardButton(program_langs[i]['fullname'], callback_data=program_langs[i]['name']),
                ]

                if i == length - 1 else

                [
                    InlineKeyboardButton(program_langs[i]['fullname'], callback_data=program_langs[i]['name']),

                    InlineKeyboardButton(program_langs[i + 1]['fullname'], callback_data=program_langs[i + 1]['name'])
                ] for i in range(0, length, 2)
            ]

        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def __confirm__keyboard(lang):

        if lang == 'uz':
            button_text = 'Tasdiqlash'
        else:
            button_text = 'Тасдиқлаш'

        return InlineKeyboardMarkup([
            [InlineKeyboardButton(button_text, callback_data='confirm')]
        ])

    def get_keyboard(self):
        return self.__keyboard
