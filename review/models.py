from django.db import models
from common.models import User


## 리뷰 모델
class Review(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewer', default=None)
    content = models.CharField(max_length=1000)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_review') # 추천수
    n_hit = models.PositiveIntegerField(default=0) # 조회수
    media_id = models.CharField(max_length=1000) # 콘텐츠 아이디

    def update_counter(self):
        self.n_hit += 1
        self.save()
    


class Review_comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_comments', default=1)
    content = models.CharField(max_length=1000)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_comment_writer', default=None)
    voter = models.ManyToManyField(User, related_name='voter_reviewcomment') # 추천수




## 찜 모델
class MyList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mylist_user')
    media_id = models.CharField(max_length=1000)

    class Meta:
        db_table = 'Mylist'
        
    def __str__(self):
        return self.user + " like " + self.content