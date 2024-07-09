from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    movie_name = State()
    genres = State()
    limit = State()
    limit_by_rating = State()
    limit_low_budget = State()
    limit_high_budget = State()
    min_rating = State()
    max_rating = State()
    movie_budget_low = State()
    movie_budget_high = State()

