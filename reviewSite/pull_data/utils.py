import pandas as pd
import urllib
from django.core.files.base import ContentFile
from pull_data.models import Post


# Test Code
def import_posts_from_csv():
    # Read CSV with Pandas
    df = pd.read_csv('https://raw.githubusercontent.com/soomerss/Imagepull/main/movie_rankings.csv',encoding='UTF-8')
    for _, row in df.iterrows():
        img_url1 = row['img']       
        img_data1 = urllib.request.urlopen(img_url1).read()
        poster_img = ContentFile(img_data1, name='poster_image.jpg')
        # Create Post object and save it to database
        post = Post.objects.create(
            movie_title=row['title'],
            poster_img=poster_img,
        )
        post.save()

