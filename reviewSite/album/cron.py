import numpy as np
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
from konlpy.tag import Okt # 형태소 분석기 Okt
from collections import Counter
import os
from datetime import datetime
from album.models import Album
import shutil


def update_info():
    """
    Ddjango-Crontab을 통해 주기적으로 실행되는 함수입니다.
    TOP10 영화의 포스터와 이들의 리뷰에 따른 워드클라우드 이미지, 영화 제목, 현재 날짜를 교체합니다.
    """

    """
    경로가 사람마다 다를 수도 있으니 주의하세요!! 만약 오류가 난다면 로그를 확인해주세요
    우분투 환경에서는 crontab 실행하려할 때 추가적으로 이 명령어 실행 $ sudo /usr/sbin/cron
    """

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    DB_PATH = os.path.join(BASE_DIR, 'db.sqlite3') # DB 경로
    IMG_SAVE_PATH = os.path.join(BASE_DIR, 'media/album_pics/') # 이미지 저장할 경로
    WORD_CLOUD_DATA_PATH = os.path.join(BASE_DIR, 'album/updateInfoFile/') # 워드클라우드 생성 위한 베이스 파일 경로


    # csv 파일 불러오기
    reviews_df = pd.read_csv(os.path.join(BASE_DIR, 'data/movie_reviews_total.csv'))
    movie_ranking_df = pd.read_csv(os.path.join(BASE_DIR, 'data/movie_rankings.csv'))
    k_stopword = pd.read_csv(WORD_CLOUD_DATA_PATH + "korean_stopword.csv")
    k_stopword = list(k_stopword['불용어'])
    k_stopword.append('영화')
    k_stopword.append('더')


    # mask로 쓸 이미지 파일 부르기
    img1 = WORD_CLOUD_DATA_PATH + 'Rotten_Tomatoes.png'
    img2 = WORD_CLOUD_DATA_PATH + 'Rotten_Tomatoes_rotten.png'
    img_white = WORD_CLOUD_DATA_PATH + 'white.png'
    mask_p = np.array(Image.open(img1))
    mask_n = np.array(Image.open(img2))
    img_w = np.array(Image.open(img_white))

    # 영화제목 콜론(:) 문자열 '-'로 변환
    reviews_df = reviews_df.replace({'movie_title':{':':'-'}},regex=True)
    movie_ranking_df = movie_ranking_df.replace({'title':{':':'-'}},regex=True)

    # rate가 문자인 경우 삭제, 이상한 단어 삭제
    reviews_df['rate'] = reviews_df['rate'].str.replace(pat=r'[ㄱ-ㅣ가-힣]+', repl= r'', regex=True)
    reviews_df = reviews_df[reviews_df.rate != '']
    reviews_df['review'] = reviews_df['review'].astype(str)
    reviews_df['rate'] = reviews_df['rate'].astype(float)

    # label 열 추가, rate가 3.5이상일때 label==1, 미만일때 label==0
    reviews_df['label'] = np.select([reviews_df.rate>=3.5], [1], default=0)

    # tokenizer 열 추가
    tokenizer = Okt()
    reviews_df['tokenized'] = reviews_df['review'].apply(tokenizer.nouns)


    # 영화 랭킹 순으로 긍정, 부정 워드 클라우드 만들기
    is_positive_comment_sufficent = False
    is_negative_comment_sufficent = False

    for i in range(0,len(movie_ranking_df)):

        matched_title_reviews_df = reviews_df.loc[reviews_df['movie_title']==movie_ranking_df['title'][i]]

        # 긍정 리뷰가 1개 이상이라면 긍정 워드클라우드 생성
        if len(matched_title_reviews_df[matched_title_reviews_df['label']==1]['tokenized'])!=0:
            is_positive_comment_sufficent = True

            positive_reviews = np.hstack(matched_title_reviews_df[matched_title_reviews_df['label']==1]['tokenized'].values)
            positive_count=Counter(positive_reviews)

            rank_text_p=dict(positive_count)


            # 불용어 제거
            temp_dic_p={}

            for key, value in rank_text_p.items():
                if key not in k_stopword:
                    temp_dic_p[key]=value

            wordcloud_p = WordCloud(
                font_path = WORD_CLOUD_DATA_PATH + 'NanumGothic.ttf',
                width = 500,
                height = 500,
                background_color = "white",
                mask = mask_p
            )

            wordcloud_p = wordcloud_p.generate_from_frequencies(temp_dic_p)
            image_colors_p = ImageColorGenerator(mask_p)


        # 부정 리뷰가 1개 이상이라면 부정 워드클라우드 생성
        if len(matched_title_reviews_df[matched_title_reviews_df['label']==0]['tokenized'])!=0:
            is_negative_comment_sufficent = True

            negative_reviews = np.hstack(matched_title_reviews_df[matched_title_reviews_df['label']==0]['tokenized'].values)
            negative_count=Counter(negative_reviews)

            rank_text_n=dict(negative_count)


            # 불용어 제거
            temp_dic_n={}
            for key, value in rank_text_n.items():
                if key not in k_stopword:
                    temp_dic_n[key]=value

            wordcloud_n = WordCloud(
                font_path = WORD_CLOUD_DATA_PATH + 'NanumGothic.ttf',
                width = 500,
                height = 500,
                background_color = "white",
                mask = mask_n
            )

            wordcloud_n = wordcloud_n.generate_from_frequencies(temp_dic_n)
            image_colors_n = ImageColorGenerator(mask_n)



        total_good_img_save_path = IMG_SAVE_PATH + str(i+1) + '.png'

        # 긍정 워드클라우드가 생성된 경우 이미지 저장
        if is_positive_comment_sufficent:
            plt.figure(figsize=(10, 10))
            plt.imshow(wordcloud_p.recolor(color_func=image_colors_p), interpolation="bilinear")
            plt.axis("off")

            # 이미지 덮어쓰기가 plt에서는 지원이 안되므로 삭제했다가 저장 새로하기
            if os.path.isfile(total_good_img_save_path):
                os.remove(total_good_img_save_path)
            plt.savefig(total_good_img_save_path)
        # 아닐 경우 흰 이미지로 대체
        else:
            shutil.copy2(img_white, total_good_img_save_path) # shutil.copy2(src, dst) : src의 파일 정보를 dst에 복사


        total_bad_img_save_path = IMG_SAVE_PATH + str(i+1) + '-1' + '.png'

        # 부정 워드클라우드가 생성된 경우 이미지 저장
        if is_negative_comment_sufficent:
            plt.figure(figsize=(10,10))
            plt.imshow(wordcloud_n.recolor(color_func=image_colors_n), interpolation="bilinear")
            plt.axis("off")

            # 이미지 덮어쓰기가 plt에서는 지원이 안되므로 삭제했다가 저장 새로하기
            if os.path.isfile(total_bad_img_save_path):
                os.remove(total_bad_img_save_path)
            plt.savefig(total_bad_img_save_path)
        # 아닐 경우 흰 이미지로 대체
        else:
            shutil.copy2(img_white, total_bad_img_save_path) # shutil.copy2(src, dst) : src의 파일 정보를 dst에 복사


        # flag 초기화
        is_positive_comment_sufficent = False
        is_negative_comment_sufficent = False


        # 포스터 변경
        poster_url = movie_ranking_df['img'][i]
        os.system("curl " + poster_url + " > " + IMG_SAVE_PATH + "%s_poster.jpg" % (str(i+1)))



        # 정보를 변경할 앨범 객체 가져오기
        album = Album.objects.get(id=i+1)

        # Title 업데이트
        title = movie_ranking_df['title'][i]
        album.title = title

        # 업데이트 날짜로 바꾸기
        album.dt_updated = datetime.now()

        # 추천한 유저 리스트 초기화
        album.positive_voters.set([])
        album.negative_voters.set([])

        # 추천수 초기화
        album.positive_votes_n = 0
        album.negative_votes_n = 0

        # 변경 사항 저장
        album.save()


    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{now} : Done web page update.') # log 확인을 위해서 종료 메시지 추가


def save_csv_from_git():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    movie_df = pd.read_csv('https://raw.githubusercontent.com/Devcourse-1th-team1-1/back-end-repo/crawling/crawlingFolder/backup/movie_rankings.csv')

    review_df = pd.read_csv('https://raw.githubusercontent.com/Devcourse-1th-team1-1/back-end-repo/crawling/crawlingFolder/backup/movie_reviews_total.csv')

    movie_df.to_csv(os.path.join(BASE_DIR, 'data/movie_rankings.csv'), index=False)
    review_df.to_csv(os.path.join(BASE_DIR, 'data/movie_reviews_total.csv'), index=False)
    print(f'{now} : save_csv_from_git')
