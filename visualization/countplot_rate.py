import numpy as np # Numpy(넘파이) 패키지 임포트
import pandas as pd # pandas(판다스) 패키지 임포트
import matplotlib.pyplot as plt # Matplotlib(맷플롯립) 패키지의 pyplot 모듈을 plt로 임포트
from matplotlib import rcParams # 한글 환경 설정을 위한 rcParams 임포트
import seaborn as sns # Seaborn(씨본) 패키지 임포트
import warnings

def setting_styles_basic():
    rcParams['font.family'] = 'Malgun Gothic' # Windows
    # rcParams['font.family'] = 'AppleGothic' # Mac
    rcParams['axes.unicode_minus'] = False # 한글 폰트 사용 시, 마이너스 기호가 깨지는 현상 방지

setting_styles_basic()

# 경고창 무시
warnings.filterwarnings('ignore')

sns.set_context('paper', # notebook, talk, poster
                rc={'font.size':15, 
                    'xtick.labelsize':15, 
                    'ytick.labelsize':15, 
                    'axes.labelsize':15})

# 파일들의 경로 
path = 'C:/Users/samsung/OneDrive - 서울과학기술대학교/바탕 화면/project_5/'

# csv 파일 불러오기
df=pd.read_csv(path+"reviews_total.csv")
df2=pd.read_csv(path+"reviews_ranking.csv")

df['rate']=df['rate'].str.replace(pat=r'[ㄱ-ㅣ가-힣]+', repl= r'', regex=True)
df=df[df.rate!='']
df['rate']=df['rate'].astype(float)

# countplot 세로
for i in range(0,len(df2)):
    # 해당 영화 제목 출력
    print(df2['title'][i])
    # 해당 영화의 리뷰들만 가져와서 새로운 df3에 저장
    df3=df.loc[df['movie_title']==df2['title'][i]]
    if len(df3)==0:
        continue
    df4=df3[['rate']]

    # plt.figure(10,8)
    sns.countplot(y='rate',
                data=df4,
                color='#D1EDE8')
    plt.title('평점분포',fontsize=20, pad=30)
    plt.title('평점분포',fontsize=15, pad=30)
    plt.ylabel('평점', fontsize=15)
    plt.xlabel('count', fontsize=15)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    # plt.show()
    plt.savefig(path+df2['title'][i]+'_count_rate.png')
    plt.clf()

#     # countplot 가로
# for i in range(0,len(df2)):
#     # 해당 영화 제목 출력
#     print(df2['title'][i])
#     # 해당 영화의 리뷰들만 가져와서 새로운 df3에 저장
#     df3=df.loc[df['movie_title']==df2['title'][i]]
#     if len(df3)==0:
#         continue
#     df4=df3[['rate']]
    
#     sns.countplot(x='rate',
#                 data=df4,
#                 color='#ecb3ff')
#     plt.title('평점분포',fontsize=20, pad=30)
#     plt.title('평점분포',fontsize=15, pad=30)
#     plt.xlabel('평점', fontsize=15)
#     plt.ylabel('count', fontsize=15)
#     plt.xticks(fontsize=12)
#     plt.yticks(fontsize=12)
#     plt.tight_layout()
#     # plt.show()
#     plt.savefig(path+df2['title'][i]+'_count_rate.png')
#     lt.clf()