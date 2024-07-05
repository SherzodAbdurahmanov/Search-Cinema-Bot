from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def gen_markup():
    # Функция , создание кнопок.
    btn_1 = KeyboardButton(text='Поиск по названию')
    btn_2 = KeyboardButton(text='Поиск по рейтингу')
    btn_3 = KeyboardButton(text='С низким бюджетом')
    btn_4 = KeyboardButton(text='С высоким бюджетом')
    btn_5 = KeyboardButton(text='История запросов')

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(btn_1, btn_2, btn_3, btn_4, btn_5)
    return keyboard
