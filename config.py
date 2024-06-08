import requests
import telebot
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Hello World !')


@bot.message_handler(commands=['movie_search'])
# """ Функция , поиск фильма/сериала по названию."""
def movie_search(message):
    bot.reply_to(message, 'Простите функция еще не готова ((')

    pass


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


if __name__ == '__main__':
    bot.infinity_polling()
