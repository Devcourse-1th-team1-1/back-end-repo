import requests
from bs4 import BeautifulSoup
import pandas as pd
import os 
from datetime import datetime


class MovieScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.movies = []
    
    def get_movies(self, url):
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        parent_tag = soup.find_all(class_='css-1qq59e8')
        netflix_tag = parent_tag[2]

        for idx, movie_li in enumerate(netflix_tag.find_all(class_='css-8y23cj')):
            movie_link = movie_li.find('a')['href']
            movie_img = movie_li.find('img')['src']
            movie_title = movie_li.find(class_='css-5yuqaa').text
            movie_mean_rate = movie_li.find(class_='average css-xgmur2').find_all('span')[1].text

            movie = dict()
            movie["date"] = datetime.now().strftime("%Y-%m-%d")
            movie["rank"] = idx + 1
            movie["title"] = movie_title
            movie["mean_rate"] = movie_mean_rate
            movie["movies_link"] = self.base_url + movie_link
            movie["img"] = movie_img
            
            self.get_movie_details(movie)
            self.movies.append(movie)
            print(movie)
        

    def get_movie_details(self, movie):
        movie_url = movie["movies_link"]
        response = requests.get(movie_url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        parent_tag = soup.find_all('article')[0]
        title = parent_tag.find(class_='css-wvh1uf-Summary eokm2781').contents[0].strip()
        year_country_genre = parent_tag.find_all(class_='css-1t00yeb-OverviewMeta eokm2782')[0].text.split('·')
        year = year_country_genre[0].strip()
        country = year_country_genre[1].strip()
        genre = year_country_genre[2].strip()
        
        try:
            time_regulation = parent_tag.find_all(class_='css-1t00yeb-OverviewMeta eokm2782')[1].text.split('·')
            time = time_regulation[0].strip()
            regulation = time_regulation[1].strip()
        except IndexError:
            time = "Unknown"
            regulation = "Unknown"

        description = parent_tag.find(class_='css-kywn6v-StyledText eb5y16b1').text.strip()

        movie["year"] = year
        movie["country"] = country
        movie["genre"] = genre
        movie["time"] = time
        movie["regulation"] = regulation
        movie["description"] = description

    def save_to_csv(self, file_name):
        df = pd.DataFrame(self.movies)
        df.to_csv(file_name, index=False, encoding='utf-8-sig')


if __name__ == "__main__":
    base_url = "https://pedia.watcha.com"
    ranking_url = "https://pedia.watcha.com/ko-KR"
    scraper = MovieScraper(base_url)
    scraper.get_movies(ranking_url)
    
    output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    file_path = os.path.join(output_folder, "movie_rankings.csv")
    scraper.save_to_csv(file_path)
    print(file_path)
    