from loader import bot


@bot.message_handler(commands=['high_budget_movie'])
# """ Функция , поиск фильмов/сериалов с высоким бюджетом. """
def high_budget_movie(message):
    bot.reply_to(message, 'Простите функция еще не готова ((')
    pass
