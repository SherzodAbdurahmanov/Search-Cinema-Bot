import requests
from config_data.config import API_KEY


def fetch_movies_by_high_budget(budget: int, limit: int) -> dict:
    """
       Функция для запроса фильмов с бюджетом ниже заданного значения
       :param budget: int
       :param limit: int
       :return: dict
    """
    base_url = 'https://api.kinopoisk.dev/v1.4/movie'
    params = {
        'page': 1,
        'limit': limit,
        'budget.value': budget
    }
    headers = {'X-API-KEY': API_KEY}
    response = requests.get(base_url, headers=headers, params=params)
    return response.json()
