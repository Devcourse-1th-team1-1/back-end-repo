from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.models import Variable
from airflow.utils.dates import days_ago
from airflow.models import XCom

from airflow import DAG
from airflow.decorators import dag, task

import pandas as pd
from datetime import datetime
import os
import time

from movie_crawler.movie_review_crawler import ReviewScraper


'''
각각의 영화 URL 마다 리뷰를 추출하고, save_reviews 함수를 호출하여 각각의 CSV 파일로 저장합니다. 
extract_reviews 함수는 ReviewScraper 클래스를 사용하여 영화 리뷰를 추출합니다. 
추출한 리뷰는 다음 태스크의 인풋으로 사용됩니다. 
save_reviews 함수는 추출한 리뷰를 CSV 파일로 저장합니다.
'''


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'max_active_runs' : 1,
    'retries': 1,
    'catchup': False,
    'tags': ['review', 'crawler'] # tags를 여기에 추가
}

def extract_reviews(**context):
    idx = context['params']['idx']
    movie_url = context["params"]["movie_url"]
    driver_path = context["params"]["driver_path"]
    scraper = ReviewScraper(movie_url = movie_url, executable_path = driver_path)
    scraper.get_reviews()
    context['ti'].xcom_push(key='movie_reviews', value=scraper.reviews)
    time.sleep(1)
    print(f"extract_reviews{idx} {len(scraper.reviews)}")



def save_reviews(**context):
    idx = context['params']['idx']
    movie_title = context["params"]["movie_title"]
    file_name = f"movie_reviews_{idx+1}.csv"
    base_dir = context["params"]["base_dir"]
    data_dir = os.path.join(base_dir, 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    save_file_name = os.path.join(data_dir, file_name)
    # Pull the reviews from XCom
    reviews = context["ti"].xcom_pull(task_ids=f'extract_reviews_{idx}', key='movie_reviews')
    print(reviews)
    # Save the reviews to a CSV file
    df = pd.DataFrame(reviews)
    df.to_csv(save_file_name, index=True)


def read_movie_info():
    movie_info = pd.read_csv("/Users/yoohajun/Airflow/dags/movie_crawler/movie_rankings.csv")
    movie_info_dict = {"movie_title": movie_info["title"], "movie_url": movie_info['movies_link']}
    return movie_info_dict


with DAG(
    'review_crawler',
    default_args=default_args,
    schedule_interval="@once"    
    ) as dag:


    movie_info = read_movie_info()

    for idx in range(10):
        movie_title = movie_info["movie_title"][idx] 
        movie_url = movie_info['movie_url'][idx] 

        extract_task = PythonOperator(
            task_id=f'extract_reviews_{idx}',
            python_callable=extract_reviews,
            params={
                'movie_url': movie_url,
                'idx': idx,
                'driver_path' : "/Users/yoohajun/Airflow/dags/movie_crawler/chromedriver"
            },
            provide_context=True  # to allow the output to be passed as an argument to the next task.
        )

        save_task = PythonOperator(
            task_id=f'save_reviews_{idx}',
            python_callable=save_reviews,
            params={
                'idx': idx,
                'movie_title': movie_title,
                'base_dir': "/Users/yoohajun/Airflow/dags/movie_crawler",
            }
        )

        extract_task >> save_task