import requests
from config_data.config import API_KEY


def fetch_movies_by_rating(min_rating: float, max_rating: float, limit: int) -> dict:
    base_url = 'https://api.kinopoisk.dev/v1.4/movie'
    params = {
        'page': 1,
        'limit': limit,
        'rating.kp': f'{min_rating}-{max_rating}'
    }
    headers = {'X-API-KEY': API_KEY}
    response = requests.get(base_url, headers=headers, params=params)
    return response.json()
