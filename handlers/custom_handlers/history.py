from loader import bot
from database.database import get_user_message_history
from telebot.types import Message


@bot.message_handler(func=lambda message: message.text == 'История запросов')
def history(message: Message) -> None:
    """
    Функция ,для просмотра истории запросов и поиска фильма/сериала
    :param message: str
    :return:
    """
    user_id = message.from_user.id

    # Retrieve message history
    messages = get_user_message_history(user_id)

    # Format the messages
    if messages:
        history_text = "Последние 10 запросов:\n\n"
        for msg in messages:
            history_text += f"{msg[1]}: {msg[0]}\n"
    else:
        history_text = "Пока нет запросов."

    bot.reply_to(message, history_text)
