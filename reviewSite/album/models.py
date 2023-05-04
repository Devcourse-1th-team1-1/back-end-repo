from django.db import models

class Album(models.Model):
    title = models.CharField(max_length=30) # 제목 30자 제한
    
    image1 = models.ImageField(upload_to='album_pics') # 영화 포스터
    image2 = models.ImageField(upload_to='album_pics', blank=True) # 긍정 클라우드
    image3 = models.ImageField(upload_to='album_pics', blank=True) # 부정 클라우드

    dt_created = models.DateTimeField(auto_now_add=True) # 글 게시 시간
    dt_updated = models.DateTimeField(auto_now=True) # 글 수정 시간

    author = models.ForeignKey('common.User', on_delete=models.CASCADE) # 리뷰 글 작성자 (Admin으로 일단)

    def __str__(self):
        return self.title
    
    
class Comment(models.Model):
    content = models.CharField(max_length=300)

    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey('common.User', on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:50]