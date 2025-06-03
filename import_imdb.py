import pandas as pd
import django
import os

import pandas as pd
import django
import os
from tqdm import tqdm

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "prs_project.settings")
django.setup()

from recommender.models import MovieDescriptions

def clean_text(text, max_length):
    if pd.isna(text):
        return ''
    return str(text)[:max_length]

def import_imdb_data(csv_path, is_top_list=False):
    df = pd.read_csv(csv_path)
    
    for _, row in tqdm(df.iterrows(), total=len(df)):
        try:
            if is_top_list:
                # Обработка топового файла
                imdb_id = row['Poster_Link'].split('/')[-2]  # Извлекаем ID из ссылки
                MovieDescriptions.objects.update_or_create(
                    imdb_id=imdb_id,
                    defaults={
                        'movie_id': imdb_id,  # Используем IMDB ID как movie_id
                        'title': clean_text(row['Series_Title'], 512),
                        'description': clean_text(row['Overview'], 1024),
                        'genres': clean_text(row['Genre'], 512)
                    }
                )
            else:
                # Обработка полного файла
                MovieDescriptions.objects.update_or_create(
                    imdb_id=row['imdb_title_id'],
                    defaults={
                        'movie_id': row['imdb_title_id'],
                        'title': clean_text(row['title'], 512),
                        'description': clean_text(row['description'], 1024),
                        'genres': clean_text(row['genre'], 512)
                    }
                )
        except Exception as e:
            print(f"Error processing row {_}: {str(e)}")
            
            import_full_imdb('IMDb_movies.csv')  # Для полной базы