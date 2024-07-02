import requests
from loader import bot
from config_data.config import API_KEY
from telebot.types import Message
from states.information import UserInfoState


@bot.message_handler(func=lambda message: message.text == 'Поиск по названию')
def movie_search(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.movie_name, message.chat.id)
    bot.send_message(message.from_user.id, 'Введите название фильма:')


@bot.message_handler(state=UserInfoState.movie_name)
def get_movie_name(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['movie_name'] = message.text

    bot.send_message(message.from_user.id, 'Отлично, теперь введите жанр фильма:')
    bot.set_state(message.from_user.id, UserInfoState.genres, message.chat.id)
    bot.register_next_step_handler(message, get_movie_genre)


def get_movie_genre(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['genres'] = message.text

    bot.send_message(message.from_user.id, 'И последнее, введите количество выводимых вариантов:')


@bot.message_handler(state=UserInfoState.genres)
def get_movie_limit(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        try:
            data['limit'] = int(message.text)

            base_url = 'https://api.kinopoisk.dev/v1.4/movie/search'
            params = {
                'page': 1,
                'limit': data['limit'],
                'query': data['movie_name']
            }
            headers = {'X-API-KEY': API_KEY}
            response = requests.get(base_url, headers=headers, params=params)
            response_data = response.json()

            if 'docs' in response_data and response_data['docs']:
                movie_data = response_data['docs'][0]
                bot.send_message(message.from_user.id,
                                 f"НАЗВАНИЕ: {movie_data['name']}\n"
                                 f"РЕЙТИНГ: {movie_data['rating']['kp']}\n"
                                 f"ГОД: {movie_data['year']}\n"
                                 f"ЖАНР: {movie_data['genres'][0]['name']}\n"
                                 f"ВОЗРАСТНОЙ РЕЙТИНГ: {movie_data['ageRating']}\n"
                                 f"ОПИСАНИЕ: {movie_data['description']}\n"
                                 f"ПОСТЕР: {movie_data['poster']['previewUrl']}"
                                 )
            else:
                bot.send_message(message.from_user.id, 'Фильмы не найдены.')

        except ValueError:
            bot.send_message(message.from_user.id, 'Количество выводимых вариантов должно быть числом!')

