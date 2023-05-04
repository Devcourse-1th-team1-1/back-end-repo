import pandas as pd
import os
from datetime import datetime

def hello_every_minute():
    print('hello')


def save_csv_from_git():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    movie_df = pd.read_csv('https://raw.githubusercontent.com/Devcourse-1th-team1-1/back-end-repo/crawling/crawlingFolder/backup/movie_rankings.csv')
    
    review_df = pd.read_csv('https://raw.githubusercontent.com/Devcourse-1th-team1-1/back-end-repo/crawling/crawlingFolder/backup/movie_reviews_total.csv')
    
    movie_df.to_csv(os.path.join(BASE_DIR, 'data/movie_rankings.csv'), index=False)
    review_df.to_csv(os.path.join(BASE_DIR, 'data/movie_reviews_total.csv'), index=False)
    print(f'{now} : save_csv_from_git')