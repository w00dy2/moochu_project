from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('moobo', views.moobo, name='moobo'), # post list 페이지
    path('post', views.post, name='post'), # post upload 페이지
    path('post_detail/<int:post_id>', views.detail, name='post_detail'), # 게시글 상세페이지
    path('post/edit/<int:post_id>/', views.post_edit, name='post_edit'), # 게시글 수정
    path('post/delete/<int:post_id>/', views.post_delete, name='post_delete'), # 게시글 삭제
    path('comment/create/post/<int:post_id>/', views.comment_create, name='comment_create'), # comment 작성
    path('comment/edit/post/<int:comment_id>/', views.comment_edit, name='comment_edit'), # 댓글 수정
    path('comment/delete/post/<int:comment_id>/', views.comment_delete, name='comment_delete'), # 댓글 삭제
    path('vote/post/<int:post_id>/', views.vote_post, name='vote_post'), # 글 정말 추천하시겠읍니까? 페이지
    path('vote/comment/<int:comment_id>/', views.vote_comment, name='vote_comment'), # 댓글 정말 추천하시겠읍니까? 페이지
    path('<int:user_id>/my_posts/', views.my_posts, name='my_posts'), 
]
