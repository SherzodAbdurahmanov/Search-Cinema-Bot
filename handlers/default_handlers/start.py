from telebot.types import Message
from loader import bot
from keyboards.reply import reply_markups


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    bot.send_message(message.from_user.id,
                     f'Привет ✋{message.from_user.full_name}\nЯ бот 🤖 который поможет вам найти фильмы/сериалы:\n'
                     'По названию:\nПо рейтингу:\nС низким бюджетом:\nС высоким бюджетом:\n'
                     'Выберите команду ниже 👇👇👇', reply_markup=reply_markups.gen_markup())
