from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    movie_name = State()
    genres = State()
    limit = State()

