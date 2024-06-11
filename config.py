import requests
import os
import telebot
from dotenv import load_dotenv
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

if not load_dotenv():
    print('Переменные окружение не загружены т.к отсутвует файд .env !')
else:
    load_dotenv()

API_KEY = os.getenv("API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)


def gen_markup() -> ReplyKeyboardMarkup:
    # Функция , создание кнопок.
    btn_1 = KeyboardButton(text='Поиск по названию')
    btn_2 = KeyboardButton(text='Поиск по рейтингу')
    btn_3 = KeyboardButton(text='С низким бюджетом')
    btn_4 = KeyboardButton(text='С высоким бюджетом')
    btn_5 = KeyboardButton(text='История запросов')

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(btn_1, btn_2, btn_3, btn_4, btn_5)
    return keyboard


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.from_user.id,
                     'Привет ✋\nЯ бот 🤖 который поможет вам найти фильмы/сериалы:\n'
                     'По названию:\nПо рейтингу:\nС низким бюджетом:\nС высоким бюджетом:\n'
                     'Выберите команду ниже 👇👇👇', reply_markup=gen_markup())


@bot.message_handler(func=lambda message: message.text == 'Поиск по названию')
# """ Функция , поиск фильма/сериала по названию."""
def movie_search(message):
    base_url = 'https://api.kinopoisk.dev/v1.4/movie/search?'
    params = {
        'page': 1,
        'limit': 10,
        'query': "Рай под ногами матерей"
    }
    headers = {'X-API-KEY': API_KEY}
    resource = 'v1.4/movie'
    response = requests.get(f"{base_url}{resource}", headers=headers, params=params)
    data = response.json()
    bot.reply_to(message, f"НАЗВАНИЕ: {data['docs'][0]['name']}\n"
                          f"РЕЙТИНГ: {data['docs'][0]['rating']['kp']}\n"
                          f"ГОД: {data['docs'][0]['year']}\n"
                          f"ЖАНР: {data['docs'][0]['genres'][0]['name']}\n"
                          f"ВОЗРАСТНОЙ РЕЙТИНГ: {data['docs'][0]['ageRating']}\n"
                          f"ОПИСАНИЕ: {data['docs'][0]['description']}\n"
                          f"ПОСТЕР: {data['docs'][0]['poster']['previewUrl']} ")


@bot.message_handler(commands=['movie_by_rating'])
# """ Функция , поиск фильма/сериала по рейтингу."""
def movie_by_rating(message):
    bot.reply_to(message, 'Простите функция еще не готова ((')
    pass


@bot.message_handler(commands=['low_budget_movie'])
# """ Функция , поиск фильмов/сериалов с низким бюджетом. """
def low_budget_movie(message):
    bot.reply_to(message, 'Простите функция еще не готова ((')
    pass


@bot.message_handler(commands=['high_budget_movie'])
# """ Функция , поиск фильмов/сериалов с высоким бюджетом. """
def high_budget_movie(message):
    bot.reply_to(message, 'Простите функция еще не готова ((')
    pass


@bot.message_handler(commands=['history'])
# """ Функция ,для просмотра истории запросов и поиска фильма/сериала"""
def history(message):
    bot.reply_to(message, 'Простите функция еще не готова ((')
    pass


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, 'Одильбек иди лучше работай зачем тебе это ?.')


if __name__ == '__main__':
    bot.infinity_polling()
