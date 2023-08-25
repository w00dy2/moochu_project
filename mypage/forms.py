from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from common.models import User
from .models import GuestBook
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class GuestBookForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), max_length=500)
    class Meta:
        model = GuestBook
        fields=['content']

class ProfileUpdateForm(forms.ModelForm):
    nickname = forms.CharField(max_length=50, required=False)
    fav_genre = forms.CharField(max_length=100, required=False)
    profile_img = forms.ImageField(required=False)
    comment = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ['nickname', 'fav_genre', 'profile_img', 'comment']