import requests
from config_data.config import API_KEY


def fetch_movies_by_title(title: str, limit: int) -> dict:
    base_url = 'https://api.kinopoisk.dev/v1.4/movie/search?'
    params = {
        'page': 1,
        'limit': limit,
        'query': title
    }
    headers = {'X-API-KEY': API_KEY}
    response = requests.get(base_url, headers=headers, params=params)
    return response.json()
