from loader import bot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from states.information import UserInfoState
from api import movie_search_api
from database.database import store_user_message


@bot.message_handler(func=lambda message: message.text == 'Поиск по названию')
def movie_search(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.movie_name, message.chat.id)
    bot.send_message(message.from_user.id, 'Введите название фильма:')


@bot.message_handler(state=UserInfoState.movie_name)
def get_movie_name(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['movie_name'] = message.text

    bot.send_message(message.from_user.id, 'Введите количество выводимых вариантов:')
    bot.set_state(message.from_user.id, UserInfoState.limit, message.chat.id)
    store_user_message(message.from_user.id, message.text)


@bot.message_handler(state=UserInfoState.limit)
def get_limit(message: Message) -> None:
    try:
        limit = int(message.text)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['limit'] = limit

            movies_data = movie_search_api.fetch_movies_by_title(data['movie_name'], data['limit'])

        if 'docs' in movies_data and movies_data['docs']:
            for movie in movies_data['docs']:
                poster_url = movie.get('poster', {}).get('previewUrl', None)
                watch_button = InlineKeyboardMarkup()
                watch_button.add(InlineKeyboardButton("Смотреть", url=f"https://www.kinopoisk.ru/film/{movie['id']}/"))
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
