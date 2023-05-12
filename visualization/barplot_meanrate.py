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

# 폰트 설정
sns.set_context('paper', # notebook, talk, poster
                rc={'font.size':10, 
                    'xtick.labelsize':10, 
                    'ytick.labelsize':10, 
                    'axes.labelsize':15})

# 파일들의 경로 
path = 'C:/Users/samsung/OneDrive - 서울과학기술대학교/바탕 화면/project_5/'

# csv 파일 불러오기
df=pd.read_csv(path+"reviews_total.csv")
df2=pd.read_csv(path+"reviews_ranking.csv")

df['rate']=df['rate'].str.replace(pat=r'[ㄱ-ㅣ가-힣]+', repl= r'', regex=True)
df=df[df.rate!='']
df['rate']=df['rate'].astype(float)

df3=df2[['title','mean_rate']]


# bar plot 저장
plt.figure(figsize=(10,8))
sns.barplot(x='title',
            y='mean_rate',
            data=df3,
            palette='Set3',
            width=0.6)
plt.xticks(rotation=45)
plt.title('평균평점 비교', fontsize=20, pad=30)
plt.xlabel('영화제목')
plt.ylabel('평균평점')
plt.yticks(np.arange(0,5.5,0.5))
plt.tight_layout()
plt.savefig(path+'mean_rate_moviecompare.png')
# plt.show()