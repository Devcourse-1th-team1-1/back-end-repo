from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.options import Options

from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By

import time
import pandas as pd
import os
import random

import multiprocessing

class ReviewScraper:
    def __init__(self, movie_url, driver=None, movie_title = None,
                 executable_path="./chromedriver"):
        
        self.movie_url = movie_url
        self.executable_path = executable_path
        self.movie_title = movie_title
        self.reviews = []
        self.driver = driver 

    @classmethod
    def driver_get(cls, executable_path):
        if os.path.exists(executable_path):
            driver_path = executable_path
        else:
            driver_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
        
        print("chromedriver path: ", driver_path)
        
        assert os.path.exists(driver_path), "Chromedriver executable not found"
        
        if os.path.exists(driver_path):
            os.chmod(driver_path, 0o755)  # chromedriver 권한 설정
        
        chrome_options = Options()
        options = [
            "--headless=new",
            "--no-sandbox"
            "--disable-gpu",
            "--start-maximized",
            # "--window-size=1980,1030",
            # "--window-size=1920,1200",
            "--ignore-certificate-errors",
            "--disable-infobars",
            "--disable-extensions",
            "--disable-dev-shm-usage"
        ]
        # ua = UserAgent(verify_ssl=False)
        # user_agent = ua.random
        # print(user_agent)
        # chrome_options.add_argument(f'user-agent={user_agent}')
        if options:
            for option in options:
                chrome_options.add_argument(option)

        # service = ChromeService(executable_path=driver_path)
        driver = webdriver.Chrome(driver_path, options=chrome_options)
        return driver

    def driver_initialize(self):
        executable_path = self.executable_path
        self.driver = self.driver if self.driver else self.driver_get(executable_path)
        
    def get_reviews(self):
        print("get_reviews ", self.movie_title)
        movie_comment_link = self.movie_url + '/comments'
        driver = self.driver
        driver.get(movie_comment_link)
        driver.implicitly_wait(4)
        
        driver.get(movie_comment_link)
        driver.implicitly_wait(15) # 웹 브라우저 창이 열리는데, 이 창이 완전히 로드되기 까지 5초간 대기
        # element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "css-10n5vg9-VisualUl ep5cwgq0")))
        prev_height = driver.execute_script("document.documentElement.style.height = '100%'; return document.body.clientHeight;")

        # prev_height = driver.execute_script("return document.body.scrollHeight") # clientHeight
        print("crawling start -> scroll height: ",prev_height)
        while len(self.reviews) < 200:
            # window.scrollTo(0,document.body.clientHeight)

            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            driver.execute_script("window.scrollTo(0, document.body.clientHeight)")
            time.sleep(2)
            current_height = driver.execute_script("return document.body.clientHeight;")
            if current_height == prev_height:
                break
            prev_height = current_height

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")
            ul_tag = soup.find(class_="css-10n5vg9-VisualUl ep5cwgq0")
            bawlbm_tags = ul_tag.find_all(class_="css-bawlbm")

            for review_object in bawlbm_tags:
                reviewer_rate = review_object.find(class_="css-4obf01")
                review_text = review_object.find(class_="css-4tkoly")
            
                if reviewer_rate and review_text:
                    try:
                        comment = {}
                        comment['movie_title'] = self.movie_title
                        comment['reviewer'] = reviewer_rate.find('a')['title']
                        comment['rate'] = reviewer_rate.find(class_='css-yqs4xl').text
                        comment['review'] = review_text.text.replace('\n', '')
                        
                        # Prevent duplicates
                        if comment not in self.reviews:
                            self.reviews.append(comment)

                    except AttributeError:
                        continue

                if len(self.reviews) >= 200:
                    break
            # print(f"현재까지 reviews: {len(self.reviews)}")
        
        # driver.quit()
        print(f"Total reviews: {self.movie_title} {len(self.reviews)}")
            

    def save_to_csv(self, movie_title, file_name):
        df = pd.DataFrame(self.reviews)
        df['movie_title'] = movie_title  # Add movie_title as a new column
        df.to_csv(file_name, index=False, encoding='utf-8-sig')


def driver_get(executable_path):
    if os.path.exists(executable_path):
        driver_path = executable_path
    else:
        driver_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
    
    print("chromedriver path: ", driver_path)
    
    assert os.path.exists(driver_path), "Chromedriver executable not found"
    
    if os.path.exists(driver_path):
        os.chmod(driver_path, 0o755)  # chromedriver 권한 설정
    
    chrome_options = Options()
    options = [
            "--headless=new",
            "--no-sandbox"
            "--disable-gpu",
            "--start-maximized",
            # "--window-size=1980,1030",
            # "--window-size=1920,1200",
            "--ignore-certificate-errors",
            "--disable-infobars",
            "--disable-extensions",
            "--disable-dev-shm-usage"
    ]
    # ua = UserAgent(verify_ssl=False)
    # user_agent = ua.random
    # chrome_options.add_argument(f'user-agent={user_agent}')
    if options:
        for option in options:
            chrome_options.add_argument(option)
    # service = ChromeService(executable_path=driver_path)
    # driver = webdriver.Chrome(service=service, options=chrome_options)
    driver = webdriver.Chrome(driver_path, options=chrome_options)
    return driver

def scrape_reviews(movie_url, movie_title, chrome_driver_path):
    
    chrome_driver = driver_get(chrome_driver_path)
    scraper = ReviewScraper(movie_url=movie_url, driver=chrome_driver, executable_path=chrome_driver_path, movie_title=movie_title)
    scraper.get_reviews()
    cnt = 0
    while len(scraper.reviews) < 5 and cnt < 3:
        scraper = ReviewScraper(movie_url=movie_url, driver=chrome_driver, executable_path=chrome_driver_path, movie_title=movie_title)
        scraper.get_reviews()
        cnt += 1
    chrome_driver.quit()
    return scraper.reviews



if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_folder = os.path.join(current_dir, "data")
    chrome_driver_path = os.path.join(current_dir, "chromedriver")
    input_data = os.path.join(input_folder, "movie_rankings.csv")
    movie_info = pd.read_csv(input_data)
    
    pool = multiprocessing.Pool(processes=2)
    results = []
    # results = pool.map(scrape_reviews, [(row['movies_link'], row['title'], chrome_driver_path) for _, row in movie_info.iterrows()])[0]
    for idx, row in movie_info.iterrows():
        movie_url = row['movies_link']
        movie_title = row['title']
        result = pool.apply_async(scrape_reviews, 
                                  args=(movie_url, movie_title, chrome_driver_path))
        results.append(result)

    pool.close()
    pool.join()
    print(results)
    
    all_reviews = []
    for result in results:
        all_reviews.extend(result.get())
        
    reviews_df = pd.DataFrame(all_reviews)
    output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    file_path = os.path.join(output_folder, "movie_reviews_total_mp.csv")
    reviews_df.to_csv(file_path, index=False, encoding='utf-8-sig')
    print(file_path)




    







