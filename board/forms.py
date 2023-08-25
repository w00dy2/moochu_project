from django import forms 
from .models import board, comment

class post_form(forms.ModelForm):
    class Meta:
        model = board
        fields = ['title', 'content']
        labels = {
            'title': '제목',
            'content': '내용'
        }



class comment_form(forms.ModelForm):
    class Meta:
        model = comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }