from django.db import models

class Album(models.Model):
    title = models.CharField(max_length=30) # 제목 30자 제한
    
    image1 = models.ImageField(upload_to='album_pics') # 최대 이미지 3장
    image2 = models.ImageField(upload_to='album_pics', blank=True)
    image3 = models.ImageField(upload_to='album_pics', blank=True)

    dt_created = models.DateTimeField(auto_now_add=True) # 글 게시 시간
    dt_updated = models.DateTimeField(auto_now=True) # 글 수정 시간

    author = models.ForeignKey('common.User', on_delete=models.CASCADE) # 앨범 글 작성자

    def __str__(self):
        return self.title