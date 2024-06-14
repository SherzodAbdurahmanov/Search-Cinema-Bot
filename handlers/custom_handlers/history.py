from loader import bot


@bot.message_handler(commands=['history'])
# """ Функция ,для просмотра истории запросов и поиска фильма/сериала"""
def history(message):
    bot.reply_to(message, 'Простите функция еще не готова ((')
    pass
