from loader import bot
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from states.information import UserInfoState
from api import movie_by_rating_api


@bot.message_handler(func=lambda message: message.text == 'Поиск по рейтингу')
def rating_search(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.min_rating, message.chat.id)
    bot.send_message(message.from_user.id, 'Введите минимальный рейтинг (0.0-10.0):')


@bot.message_handler(state=UserInfoState.min_rating)
def get_min_rating(message: Message) -> None:
    try:
        min_rating = float(message.text)
        if 0.0 <= min_rating <= 10.0:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['min_rating'] = min_rating
            bot.send_message(message.from_user.id, 'Введите максимальный рейтинг (0.0-10.0):')
            bot.set_state(message.from_user.id, UserInfoState.max_rating, message.chat.id)
        else:
            bot.send_message(message.from_user.id, 'Пожалуйста, введите значение в диапазоне 0.0-10.0:')
    except ValueError:
        bot.send_message(message.from_user.id, 'Пожалуйста, введите число.')


@bot.message_handler(state=UserInfoState.max_rating)
def get_max_rating(message: Message) -> None:
    try:
        max_rating = float(message.text)
        if 0.0 <= max_rating <= 10.0:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['max_rating'] = max_rating
            bot.send_message(message.from_user.id, 'Введите количество выводимых вариантов:')
            bot.set_state(message.from_user.id, UserInfoState.limit_by_rating, message.chat.id)
        else:
            bot.send_message(message.from_user.id, 'Пожалуйста, введите значение в диапазоне 0.0-10.0:')
    except ValueError:
        bot.send_message(message.from_user.id, 'Пожалуйста, введите число.')


@bot.message_handler(state=UserInfoState.limit_by_rating)
def get_limit(message: Message) -> None:
    try:
        limit = int(message.text)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['limit'] = limit

            movies_data = movie_by_rating_api.fetch_movies_by_rating(data['min_rating'], data['max_rating'],
                                                                     data['limit'])
        if 'docs' in movies_data and movies_data['docs']:
            for movie in movies_data['docs']:
                poster_url = movie.get('poster', {}).get('previewUrl', None)
                watch_button = InlineKeyboardMarkup()
                watch_button.add(
                    InlineKeyboardButton("Смотреть", url=f"https://www.kinopoisk.ru/film/{movie['id']}/"))
                movie_info = (f"НАЗВАНИЕ: {movie['name']}\n"
                              f"РЕЙТИНГ: {movie['rating']['kp']}\n"
                              f"ГОД: {movie['year']}\n"
                              f"ЖАНР: {movie['genres'][0]['name']}\n"
                              f"ВОЗРАСТНОЙ РЕЙТИНГ: {movie['ageRating']}\n"
                              f"ОПИСАНИЕ: {movie['description']}\n")

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
