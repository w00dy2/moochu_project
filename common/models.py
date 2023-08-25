from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    nickname = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=1000)
    gender = models.CharField(max_length=15)
    birth = models.DateField()
    fav_genre = models.CharField(max_length=100, null=True)# null을 허용해도 될까?
    created_at = models.DateField(auto_now_add=True)
    temp = models.DecimalField(max_digits=5, decimal_places=2,default=36.5)
    profile_img = models.ImageField(upload_to="profiles/", default="profiles/chuchu.png")
    comment = models.CharField(max_length=100, default="한줄소개가 아직 없습니다.")
    # delete column
    first_name = None
    last_name = None
    last_login = None
    date_joined = None
    def __str__(self):
        return self.email
    
    def get_profile_image_url(self):
        if self.profile_img:
            return self.profile_img.url
        else:
            return settings.DEFAULT_PROFILE_IMAGE

    def __str__(self):
        return self.nickname

class follow(models.Model):
    follower = models.IntegerField()
    following = models.IntegerField()

class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    genre = models.CharField(max_length=10, unique=True)  # 테이블 열 이름과 일치하도록 변경
    class Meta:
        db_table = 'genres2'  # 원래 있던 final.genres2를 메타로 설정
    def __str__(self):
        return self.genre
    
class SelectedGenre(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)  # ForeignKey로 변경

    class Meta:
        unique_together = ['user', 'genre']

        
class MovieRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE )
    media_id = models.CharField(max_length=1000)
    rating = models.FloatField()

    def __str__(self):
        return f"{self.user.nickname} rated '{self.media_id}' with {self.rating} points"