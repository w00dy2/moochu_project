from django.db import models
from common.models import User

# Create your models here.
class follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')



class GuestBook(models.Model):
    main = models.ForeignKey(User, on_delete=models.CASCADE, related_name='main')
    writer = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='writer')
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return str(self.main)
    
class MyToplist(models.Model):
    writer = models.ForeignKey(User,on_delete=models.CASCADE, related_name='Toplist_user')
    media_id = models.CharField(max_length=1000)


    class Meta:
        db_table = 'Toplist'
        