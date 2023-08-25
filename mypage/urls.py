from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'mypage'

urlpatterns = [
    ## 홈 
    path('<str:nickname>/', views.home, name="home"),
                ## 인생작 추가 및 삭제 
    path('<str:nickname>/Toplist/', views.Toplist, name="Toplist"),
    path('<str:nickname>/Toplist/delete', views.top_del, name="delete"),
    
    ## 찜 
    path('<str:nickname>/mylist/', views.mylist, name="mylist"),

    ## 리뷰 & 평점 
    path('<str:nickname>/reviews/', views.reviews, name="reviews"),
                ## 사용자의 리뷰 전체 list
    path('<str:nickname>/reviews/All/', views.reviews_total, name="reviews_total"),
                ## 사용자의 평점 전체 list
    path('<str:nickname>/votes/', views.votes, name="votes"), 

    ## 방명록
    path('<str:nickname>/guestbook/', views.guestbook, name="book"),
    path('guestbook/<int:guestbook_id>/', views.guestbook_detail, name="book_detail"), ## 방명록 삭제

    ## 프로필 수정 
    path('<int:user_id>/edit', views.edit, name="edit"),
    
    ## 팔로우 신청
    path('<str:nickname>/follow/', views.follow, name="follow"),
    path('follow/<int:follow_id>', views.follower, name="follower"), ## 팔로우 취소
]