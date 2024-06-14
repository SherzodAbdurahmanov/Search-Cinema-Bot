from loader import bot


@bot.message_handler(commands=['low_budget_movie'])
# """ Функция , поиск фильмов/сериалов с низким бюджетом. """
def low_budget_movie(message):
    bot.reply_to(message, 'Простите функция еще не готова ((')
    pass
