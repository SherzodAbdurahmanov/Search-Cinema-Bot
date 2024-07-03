from loader import bot
from telebot.types import Message
from states.information import UserInfoState
from api import movie_by_rating_api


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


@bot.message_handler(state=UserInfoState.limit)
def get_limit(message: Message) -> None:
    try:
        limit = int(message.text)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['limit'] = limit

        movie_data = movie_by_rating_api.fetch_movies_by_rating(data['min_rating'], data['max_rating'], data['limit'])

        if 'docs' in movie_data and movie_data['docs']:
            movie = movie_data['docs'][0]
            poster_url = movie.get('poster', {}).get('previewUrl', 'Постер не доступен')
            bot.send_message(message.from_user.id,
                             f"НАЗВАНИЕ: {movie['name']}\n"
                             f"РЕЙТИНГ: {movie['rating']['kp']}\n"
                             f"ГОД: {movie['year']}\n"
                             f"ЖАНР: {movie['genres'][0]['name']}\n"
                             f"ВОЗРАСТНОЙ РЕЙТИНГ: {movie['ageRating']}\n"
                             f"ОПИСАНИЕ: {movie['description']}\n"
                             f"ПОСТЕР: {poster_url}"
                             )
        else:
            bot.send_message(message.from_user.id, 'Фильмы не найдены.')

    except ValueError:

        bot.send_message(message.from_user.id, 'Пожалуйста, введите число.')
    # Сброс состояния пользователя
    bot.delete_state(message.from_user.id, message.chat.id)
