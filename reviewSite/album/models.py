from django.db import models

class Album(models.Model):
    
    title = models.CharField(max_length=30) # 제목 30자 제한  
    poster_src = models.TextField() # 영화 포스터 이미지 src
    good_cloud_img = models.ImageField(upload_to='album_pics/good_word_cloud') # 긍정 클라우드
    bad_cloud_img = models.ImageField(upload_to='album_pics/bad_word_cloud') # 부정 클라우드

    dt_created = models.DateTimeField(auto_now_add=True) # 글 게시 시간
    dt_updated = models.DateTimeField(auto_now=True) # 글 수정 시간

    author = models.ForeignKey('common.User', on_delete=models.CASCADE) # 리뷰 글 작성자 (Admin으로 일단)

    positive_votes_n = models.PositiveIntegerField(default=0)
    positive_voters = models.ManyToManyField('common.User', related_name='liked_albums')
    negative_votes_n = models.PositiveIntegerField(default=0)
    negative_voters = models.ManyToManyField('common.User', related_name='disliked_albums')

    def update_positive_votes(self, user):
        if user not in self.positive_voters.all() and user not in self.negative_voters.all():
            self.positive_votes_n += 1
            self.positive_voters.add(user)
            self.save()

    def update_negative_votes(self, user):
        if user not in self.negative_voters.all() and user not in self.positive_voters.all():
            self.negative_votes_n += 1
            self.negative_voters.add(user)
            self.save()

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
