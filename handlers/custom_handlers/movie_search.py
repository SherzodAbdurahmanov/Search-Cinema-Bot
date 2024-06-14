import requests
from loader import bot
from config_data.config import API_KEY
from telebot.types import Message
from states.information import UserInfoState


@bot.message_handler(func=lambda message: message.text == 'Поиск по названию')
# """ Функция , поиск фильма/сериала по названию."""
def movie_search(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfoState.movie_name, message.chat.id)
    bot.send_message(message.from_user.id, 'Введите название фильма:')


@bot.message_handler(state=UserInfoState.movie_name)
def get_movie_name(message: Message) -> None:
    bot.send_message(message.from_user.id, 'Отлично , теперь введите жанр фильма:')
    bot.set_state(message.from_user.id, UserInfoState.genres, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['movie_name'] = message.text


@bot.message_handler(state=UserInfoState.genres)
def get_movie_name(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'И последнее , введите количество выводимых вариантов:')
        bot.set_state(message.from_user.id, UserInfoState.limit, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['genres'] = message.text
    else:
        bot.send_message(message.from_user.id, 'Количество выводимых вариантов может быть только числом !')


@bot.message_handler(state=UserInfoState.limit)
def get_movie_name(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['limit'] = message.text
    bot.send_message(message.from_user.id, 'Вот что нашлось 👇👇👇')

    base_url = 'https://api.kinopoisk.dev/v1.4/movie/search?'
    params = {
        'page': 1,
        'limit': data['limit'],
        'query': data['movie_name ']
    }
    headers = {'X-API-KEY': API_KEY}
    resource = 'v1.4/movie'
    response = requests.get(f"{base_url}{resource}", headers=headers, params=params)
    data = response.json()
    bot.reply_to(message, f"НАЗВАНИЕ: {data['docs'][0]['name']}\n"
                          f"РЕЙТИНГ: {data['docs'][0]['rating']['kp']}\n"
                          f"ГОД: {data['docs'][0]['year']}\n"
                          f"ЖАНР: {data['docs'][0]['genres'][0]['name']}\n"
                          f"ВОЗРАСТНОЙ РЕЙТИНГ: {data['docs'][0]['ageRating']}\n"
                          f"ОПИСАНИЕ: {data['docs'][0]['description']}\n"
                          f"ПОСТЕР: {data['docs'][0]['poster']['previewUrl']} ")
