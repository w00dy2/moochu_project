from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'review'

urlpatterns =[
    path('<str:movie_id>/detail/media/rating', views.media_rating, name='media_rating'),
    path('', views.review, name="review"),
    path('<str:movie_id>/', views.review_by_id, name="review_by_id"),
    
    path('<str:movie_id>/upload/', views.review_upload, name='review_upload'),
    path('<str:movie_id>/detail/<int:review_id>/', views.review_detail, name='review_detail'),
    path('review/edit/<str:movie_id>/<int:review_id>/', views.review_edit, name='review_edit'),
    path('review/delete/<int:review_id>/', views.review_delete, name='review_delete'), 

    path('review/comment/create/<int:review_id>/', views.review_comment_create, name='review_comment_create'), # comment 작성
    path('review/comment/edit/<int:review_comment_id>/', views.review_comment_edit, name='review_comment_edit'), # 댓글 수정
    path('review/comment/delete/<int:review_comment_id>/', views.review_comment_delete, name='review_comment_delete'), # 댓글 삭제
    
    path('vote/review/<int:review_id>/', views.vote_review, name='vote_review'), 
    # path('vote/comment/<int:review_comment_id>/', views.vote_review_comment, name='vote_review_comment'), 
]