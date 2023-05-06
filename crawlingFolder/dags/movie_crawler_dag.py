import pandas as pd
import requests
from bs4 import BeautifulSoup
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.utils.dates import days_ago

from movie_crawler.movie_ranking_info import MovieScraper

'''
'get_movie_rankings'라는 하나의 태스크를 가지고 있습니다. 
이 태스크는 get_movie_rankings 함수를 실행하여 영화 순위 데이터를 가져옵니다. 
Airflow는 이 태스크가 매일 실행됩니다.
'''
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1), 
    # 'backfill': False, # 'start_date' 이후의 모든 DAG 인스턴스를 실행합니다.
    'catchup': False,
    'max_active_runs' : 1,    
    'retries': 1,
    'tags' : ['movie_info', 'crawler']
}

dag = DAG('movie_scraper', default_args=default_args, schedule_interval='@once')

def get_movie_rankings():
    base_url = "https://pedia.watcha.com"
    ranking_url = "https://pedia.watcha.com/ko-KR"
    scraper = MovieScraper(base_url)
    scraper.get_movies(ranking_url)
    scraper.save_to_csv("/Users/yoohajun/Airflow/dags/movie_crawler/movie_rankings.csv")
    
t1 = PythonOperator(
    task_id='get_movie_rankings',
    python_callable=get_movie_rankings,
    dag=dag
)