import requests
import django
import os
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moviegeek.settings')
django.setup()

from movies.models import Movie, MovieDescription

API_KEY = '8c72e3d1'
BASE_URL = 'http://www.omdbapi.com/'

def fetch_descriptions():
    movies = Movie.objects.all()[:1000]  # Первые 1000 фильмов
    for movie in movies:
        try:
            response = requests.get(BASE_URL, params={'t': movie.title, 'apikey': API_KEY})
            data = response.json()
            if data.get('Plot'):
                MovieDescription.objects.update_or_create(
                    movie=movie,
                    defaults={'description': data['Plot']}
                )
                print(f"Успешно: {movie.title}")
            time.sleep(1)  # Ограничение запросов
        except Exception as e:
            print(f"Ошибка: {movie.title} — {e}")

fetch_descriptions()