from loader import bot


@bot.message_handler(commands=['movie_by_rating'])
# """ Функция , поиск фильма/сериала по рейтингу."""
def movie_by_rating(message):
    bot.reply_to(message, 'Простите функция еще не готова ((')
    pass
