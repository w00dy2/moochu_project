from django import forms 
from .models import Review, Review_comment

class review_form(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']
        labels = {
            'content': '내용'
        }



class review_comment_form(forms.ModelForm):
    class Meta:
        model = Review_comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }