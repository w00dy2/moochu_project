# review_extras.py
from django import template
from review.views import get_movie_data
from django.utils.text import Truncator
from django.utils.html import strip_tags
import requests

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)



@register.filter
def get_movie_data_by_id(movie_id):
    return get_movie_data(movie_id)


@register.filter
def text_cut(text):
    # 첫 4줄까지만 유지하고, 더 많은 줄이 있을 경우 4번째 줄까지만 보여줌
    lines = text.split('<br>', 4)
    truncated_text = '<br>'.join(lines[:4])
    return Truncator(truncated_text).chars(70, truncate=" ...")

@register.filter
def url_exists(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.RequestException:
        return False