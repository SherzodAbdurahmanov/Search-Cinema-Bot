from loader import bot
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from states.information import UserInfoState
from api import high_budget_api


# Обработчик команды "Поиск с высоким бюджетом"
@bot.message_handler(func=lambda message: message.text == 'С высоким бюджетом')
def high_budget_search(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.movie_budget_high, message.chat.id)
    bot.send_message(message.from_user.id, 'Введите минимальный бюджет фильма в долларах США (например, 50000000):')


# Обработчик состояния получения бюджета фильма
@bot.message_handler(state=UserInfoState.movie_budget_high)
def get_high_movie_budget(message: Message) -> None:
    try:
        budget = int(message.text)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['movie_budget_high'] = budget

        bot.send_message(message.from_user.id, 'Введите количество выводимых вариантов:')
        bot.set_state(message.from_user.id, UserInfoState.limit_high_budget, message.chat.id)
    except ValueError:
        bot.send_message(message.from_user.id, 'Пожалуйста, введите число.')


# Обработчик состояния получения количества выводимых вариантов
@bot.message_handler(state=UserInfoState.limit_high_budget)
def get_high_limit(message: Message) -> None:
    try:
        limit = int(message.text)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['limit'] = limit

        movies_data = high_budget_api.fetch_movies_by_high_budget(data['movie_budget_high'], data['limit'])

        if 'docs' in movies_data and movies_data['docs']:
            for movie in movies_data['docs']:
                poster_url = movie.get('poster', {}).get('previewUrl', None)
                budget = movie.get('budget', {}).get('value', 'Неизвестен')
                watch_button = InlineKeyboardMarkup()
                watch_button.add(InlineKeyboardButton("Смотреть", url=f"https://www.kinopoisk.ru/film/{movie['id']}/"))
                movie_info = (f"НАЗВАНИЕ: {movie['name']}\n"
                              f"РЕЙТИНГ: {movie['rating']['kp']}\n"
                              f"ГОД: {movie['year']}\n"
                              f"ЖАНР: {movie['genres'][0]['name']}\n"
                              f"ВОЗРАСТНОЙ РЕЙТИНГ: {movie['ageRating']}\n"
                              f"ОПИСАНИЕ: {movie['description']}\n"
                              f"БЮДЖЕТ: {budget}\n")

                if poster_url:
                    bot.send_photo(message.from_user.id, poster_url, caption=movie_info, reply_markup=watch_button)
                else:
                    bot.send_message(message.from_user.id, movie_info, reply_markup=watch_button)
        else:
            bot.send_message(message.from_user.id, 'Фильмы не найдены.')
    except ValueError:
        bot.send_message(message.from_user.id, 'Пожалуйста, введите число.')

    # Сброс состояния пользователя
    bot.delete_state(message.from_user.id, message.chat.id)
