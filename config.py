from dotenv import load_dotenv
import telebot
# import os
#
# load_dotenv()
# BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot('7236698555:AAF9spRlQ8ukGQJhEp7Rfh_qoG0try_eJCo')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Hello World !')


if __name__ == '__main__':
    bot.infinity_polling()
