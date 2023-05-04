import numpy as np
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import pandas as pd
from konlpy.tag import Okt # 형태소 분석기 Okt
from collections import Counter
import os
import sqlite3

"""
경로가 사람마다 달라지니까 주의하세요!! update_info 안에서 print(os.getcwd())로 확인하기
"""
DB_PATH = "ttt/back-end-repo/reviewSite/db.sqlite3" # DB 경로
IMG_SAVE_PATH = 'ttt/back-end-repo/reviewSite/media/album_pics/' # 이미지 저장할 경로
PATH = 'ttt/back-end-repo/reviewSite/album/updateInfoFile/' # 워드클라우드 생성 위한 베이스 파일 경로


def update_info():
    """
    Ddjango-Crontab을 통해 주기적으로 실행되는 함수입니다.
    TOP10 영화의 포스터와 이들의 리뷰에 따른 워드클라우드 이미지, 영화 제목, 현재 날짜를 교체합니다.
    """

    # csv 파일 불러오기
    df = pd.read_csv(PATH + "reviews_total.csv")
    df2 = pd.read_csv(PATH + "reviews_ranking.csv")
    k_stopword = pd.read_csv(PATH + "korean_stopword.csv")
    k_stopword = list(k_stopword['불용어'])
    k_stopword.append('영화')
    k_stopword.append('더')


    # mask로 쓸 이미지 파일 부르기
    img1 = PATH + 'Rotten_Tomatoes.png'
    img2 = PATH + 'Rotten_Tomatoes_rotten.png'
    mask_p = np.array(Image.open(img1))
    mask_n = np.array(Image.open(img2))


    # rate가 문자인 경우 삭제, 이상한 단어 삭제
    df['rate'] = df['rate'].str.replace(pat=r'[ㄱ-ㅣ가-힣]+', repl= r'', regex=True)
    df = df[df.rate != '']
    df['review'] = df['review'].astype(str)
    df['rate'] = df['rate'].astype(float)

    # label 열 추가, rate가 3.5이상일때 label==1, 미만일때 label==0
    df['label'] = np.select([df.rate>=3.5], [1], default=0)

    # tokenizer 열 추가
    tokenizer = Okt()
    df['tokenized'] = df['review'].apply(tokenizer.nouns)


    # DB 연결
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()


    # 영화 랭킹 순으로 긍정, 부정 워드 클라우드 만들기
    for i in range(0,len(df2)):

        df3 = df.loc[df['movie_title']==df2['title'][i]]

        # 해당 영화에 리뷰가 없을경우 continue
        if len(df3) == 0:
            continue
        positive_reviews = np.hstack(df3[df3['label']==1]['tokenized'].values)
        negative_reviews = np.hstack(df3[df3['label']==0]['tokenized'].values)

        positive_count=Counter(positive_reviews)
        negative_count=Counter(negative_reviews)

        rank_text_p=dict(positive_count)
        rank_text_n=dict(negative_count)


        # 불용어 제거
        temp_dic_p={}

        for key, value in rank_text_p.items():
            if key not in k_stopword:
                temp_dic_p[key]=value

        temp_dic_n={}
        for key, value in rank_text_n.items():
            if key not in k_stopword:
                temp_dic_n[key]=value


        wordcloud_p = WordCloud(
            font_path = PATH + 'NanumGothic.ttf',
            width = 500,
            height = 500,
            background_color = "white",
            mask = mask_p
        )

        wordcloud_n = WordCloud(
            font_path = PATH + 'NanumGothic.ttf',
            width = 500,
            height = 500,
            background_color = "white",
            mask = mask_n
        )

        wordcloud_p = wordcloud_p.generate_from_frequencies(temp_dic_p)
        wordcloud_n = wordcloud_n.generate_from_frequencies(temp_dic_n)
        image_colors_p = ImageColorGenerator(mask_p)
        image_colors_n = ImageColorGenerator(mask_n)


        # Title 업데이트
        title = df2['title'][i]
        query = "UPDATE album_album SET title = '%s' WHERE id = '%s'" % (title, str(i+1))
        cur.execute(query) # 제목 업데이트하는 쿼리 실행

        query2 = "UPDATE album_album SET dt_created = datetime('now') WHERE id = '%s'" % (str(i+1))
        cur.execute(query2) # 업데이트 날짜로 바꾸는 쿼리 실행

        conn.commit() # DB에 반영

        #긍정리뷰 이미지 저장
        plt.figure(figsize=(10, 10))
        plt.imshow(wordcloud_p.recolor(color_func=image_colors_p), interpolation="bilinear")
        plt.axis("off")

        total_good_img_save_path = IMG_SAVE_PATH + str(i+1) + '.png'

        # 이미지 덮어쓰기가 plt에서는 지원이 안되므로 삭제했다가 저장 새로하기
        if os.path.isfile(total_good_img_save_path):
            os.remove(total_good_img_save_path)

        plt.savefig(total_good_img_save_path)

        #부정리뷰 이미지 저장
        plt.figure(figsize=(10,10))
        plt.imshow(wordcloud_n.recolor(color_func=image_colors_n), interpolation="bilinear")
        plt.axis("off")

        total_bad_img_save_path = IMG_SAVE_PATH + str(i+1) + '-1' + '.png'
            
        # 이미지 덮어쓰기가 plt에서는 지원이 안되므로 삭제했다가 저장 새로하기
        if os.path.isfile(total_bad_img_save_path):
            os.remove(total_bad_img_save_path)
            
        plt.savefig(total_bad_img_save_path)

        # 포스터 변경
        poster_url = df2['img'][i]
        os.system("curl " + poster_url + " > " + IMG_SAVE_PATH + "%s_poster.jpg" % (str(i+1)))

    # for문 끝나고 DB 연결 해제
    cur.close()
    conn.close()

    print('Done.') # log 확인을 위해서 종료 메시지 추가