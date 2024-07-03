import requests
from config_data.config import API_KEY


def fetch_movies(movie_name: str, limit: int) -> dict:
    base_url = 'https://api.kinopoisk.dev/v1.4/movie/search'
    params = {
        'page': 1,
        'limit': limit,
        'query': movie_name
    }
    headers = {'X-API-KEY': API_KEY}
    response = requests.get(base_url, headers=headers, params=params)
    return response.json()
