from django.urls import path
from . import views

app_name = 'moochu'

urlpatterns =[
    path('', views.mainpage, name="main"),
    path('coming_next', views.coming_next, name='coming_next'),
    path('<str:media_type>/<str:ott>/', views.ott_media_list, name='ott_media_list'),
    path('<str:media_type>/<str:ott>/genre_filter/', views.genre_filter, name='genre_filter'),
    path('<str:movie_id>/', views.movie_detail, name='movie_detail'),

]