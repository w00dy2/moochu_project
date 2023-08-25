from django.db import models
from common.models import User


class board(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='board_writer', default=None)
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=1000)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_post')
    n_hit = models.PositiveIntegerField(default=0)

    def update_counter(self):
        self.n_hit += 1
        self.save()



class comment(models.Model):
    board = models.ForeignKey(board, on_delete=models.CASCADE, related_name='comments', default=1)
    content = models.CharField(max_length=1000)
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_writer', default=None)
    voter = models.ManyToManyField(User, related_name='voter_comment')

