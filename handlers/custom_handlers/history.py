from telebot.types import Message
from database.database import SearchHistory
from loader import bot


@bot.message_handler(func=lambda message: message.text == 'История запросов')
def show_search_history(message: Message) -> None:
    """
    Обработчик команды  "История запрсов"
    :param message: str
    """
    history = SearchHistory.select().where(SearchHistory.user_id == message.from_user.id).order_by(
        SearchHistory.timestamp.desc()).limit(10)
    if history:
        for record in history:
            bot.send_message(message.from_user.id, f"{record.timestamp}: {record.query_value}")
    else:
        bot.send_message(message.from_user.id, 'История запросов пуста.')
