from django.db import models

# Create your models here.
class Post(models.Model):
    movie_title = models.CharField(max_length=50)
    good_img = models.ImageField(verbose_name="positive_cloud",null=True,upload_to='good_img/')
    bad_img = models.ImageField(verbose_name="negative_cloud",null=True,upload_to='bad_img/')
    poster_img = models.ImageField(verbose_name="poster",upload_to='movie_poster/')