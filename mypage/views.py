from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view
from urllib3 import HTTPResponse
from rest_framework.response import Response
from .forms import GuestBookForm,ProfileUpdateForm
from . import models
from common.models import MovieRating
from moochu.models import Media
from review.models import Review, Review_comment, MyList
from collections import OrderedDict
import logging
logger=logging.getLogger('mypage')

## 마이페이지에 공통으로 보낼 데이터 
def profile_data(nickname, request):
    ## 현재 로그인한 사용자
    writer_id = request.user.id
    writer = get_object_or_404(models.User, id=writer_id)
    ## 마이페이지의 주인 
    master = get_object_or_404(models.User, nickname=nickname)
    ## 주인을 팔로우하는 사람들 목록
    following = models.follow.objects.filter(follower=master.id)
    ## 주인이 팔로우하는 사람들 목록
    follower = models.follow.objects.filter(following=master.id)
    ## 현재 로그인한 사용자가 주인을 팔로우 하는지 여부
    allow = models.follow.objects.filter(follower=writer, following=master).exists()

    ## 팔로워, 팔로잉 숫자 파악
    follower_count = follower.count() or 0
    following_count = following.count() or 0

    profile_data = {
        "master": master,
        "writer": writer,
        "follower_count": follower_count,
        "following_count": following_count,
        "allow": allow,
        "follower": follower,
        "following": following,
    }

    return profile_data


@api_view(['GET'])
def home(request, nickname):
    profile = profile_data(nickname, request)
    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        user_id = None
    info_string='main'
    logger.info(f'mypage,{info_string}', extra={'user_id': user_id})
    ## 이제 인생 명작 리스트 보내기
    toplist = {"toplist":models.MyToplist.objects.filter(writer=profile['master'].id)[:5]}
    profile.update(toplist)
                    ## 코드 ## 
    return render(request, 'mypage/mypage.html', profile)



@api_view(['GET'])
def mylist(request, nickname):
    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        user_id = None
    info_string='mylist'
    logger.info(f'mypage,{info_string}', extra={'user_id': user_id})
    
    form = profile_data(nickname, request)
    print(request.user.id)
    mylist = MyList.objects.filter(user_id=form['master'].id)
    for x in mylist:
        x.media_id = str(x.media_id)
    mylist={"mylist":mylist}
    form.update(mylist)
    return render(request, 'mypage/mylist.html', form)


def reviews(request, nickname):
    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        user_id = None
    info_string='reviews'
    logger.info(f'mypage,{info_string}', extra={'user_id': user_id})
    profile = profile_data(nickname, request)
    reviews = {"reviews": Review.objects.filter(writer_id=profile['master'].id)}
        ## 평점 데이터도 같이 보내야함

    profile.update(reviews)
    votes = {"votes": MovieRating.objects.filter(user=profile['master'].id)}
    profile.update(votes)
    return render(request, 'mypage/user_activity.html', profile)



@api_view(['GET','POST'])
def guestbook(request, nickname):
    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        user_id = None
    info_string='guestbook'
    logger.info(f'mypage,{info_string}', extra={'user_id': user_id})
    if request.method == 'POST':
        form = GuestBookForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            master = get_object_or_404(models.User, nickname=nickname)
            writer_id = request.user.id
            master_id = models.User.objects.get(id=master.id)
            writer_user = models.User.objects.get(id=writer_id)

            models.GuestBook.objects.create(
                content=content,
                main=master_id,
                writer=writer_user
            )
            return redirect('mypage:book' ,master.nickname)
    
    
    elif request.method=='GET':
        form = profile_data(nickname, request)
        book ={"book": models.GuestBook.objects.filter(main=form['master'].id).order_by('-created_at') } 
        form.update(book)
        
        return render(request, 'mypage/book.html', form)



@api_view(['DELETE'])
def guestbook_detail(request, guestbook_id):
    if request.method == 'DELETE':
        book_item = models.GuestBook.objects.filter(id=guestbook_id)
        book_item.delete()

        return Response(status=200)



@api_view(['PUT','GET'])
def edit(request, user_id):
    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        user_id = None
    info_string='edit'
    logger.info(f'mypage,{info_string}', extra={'user_id': user_id})
    if request.method == 'PUT':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            nickname = form.cleaned_data['nickname']
            print(form.cleaned_data['nickname'])
            return Response(status=200)
             #return redirect('mypage:home', nickname)
    elif request.method == 'GET':
        form = ProfileUpdateForm(instance=request.user)
        nickname = request.user.nickname
        context = profile_data(nickname, request)
        context.update({"form":form})
        return render(request, 'mypage/edit.html', context)





## 사용자의 리뷰 전체 list
def reviews_total(request, nickname):
    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        user_id = None
    info_string='reviwes_total'
    logger.info(f'mypage,{info_string}', extra={'user_id': user_id})
    profile = profile_data(nickname, request)
    reviews = {"reviews": Review.objects.filter(writer_id=profile['master'].id)}
        ## 평점 데이터도 같이 보내야함
    profile.update(reviews)
    return render(request, 'mypage/reviews.html', profile)


## 사용자의 평점 전체 list
def votes(request, nickname):
    profile = profile_data(nickname, request)
    
                ######## 평점 데이터 보내야 함 #############
    votes = {"votes": MovieRating.objects.filter(user=profile['master'].id)}
    profile.update(votes)
    return render(request, 'mypage/votes.html', profile)



@api_view(['POST','DELETE', 'GET'])
def follow(request, nickname):
    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        user_id = None
    info_string='follow'
    logger.info(f'mypage,{info_string}', extra={'user_id': user_id})
    if request.method == 'POST':
        # master_id = request.POST.get('master_id')
        master = models.User.objects.get(nickname= nickname)
        # follower 테이블에 입력하는 로직
        models.follow.objects.create(follower=request.user, following= master)
        
        return redirect('mypage:home', nickname )
    elif request.method == 'DELETE':
        master = models.User.objects.get(nickname= nickname)
        models.follow.objects.get(follower=request.user, following= master).delete()
        return Response(status=200)
    elif request.method =='GET':
        return redirect('mypage:home', nickname)

    

@api_view(['DELETE'])
def follower(request, follow_id):
    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        user_id = None
    info_string='follower'
    logger.info(f'mypage,{info_string}', extra={'user_id': user_id})
    if request.method == 'DELETE':
        models.follow.objects.get(id=follow_id).delete()
        
        
        return Response(status=200)
    
@api_view(['GET', 'POST'])
def Toplist(request, nickname):
    if request.method=='GET':
        profile = profile_data(nickname, request)
        reviews = Review.objects.filter(writer_id=profile['master'].id)

        media_ids = set(review.media_id for review in reviews)


        toplist_media_ids = set([top.media_id for top in models.MyToplist.objects.filter(writer=profile['master'].id)])
        print(toplist_media_ids)
        media = []
        media.append(media_ids-toplist_media_ids)
        
        profile.update({'reviews': list(media)[0]})
        toplist = {"toplist": models.MyToplist.objects.filter(writer=profile['master'].id)}
        profile.update(toplist)
        return render(request, 'mypage/Toplist.html', profile)
    
    elif request.method=='POST':
        # 사용자가 선택한 영화 id 리스트를 POST 데이터에서 추출합니다.
        selected_medias = request.POST.getlist("media_id")

        for media in selected_medias:
            models.MyToplist.objects.create(writer=request.user, media_id=media)

        return redirect('mypage:home', nickname)
    
def top_del(request, nickname):
    if request.method == 'POST':
        selected_medias = request.POST.getlist("media_id")
        for media in selected_medias:
                models.MyToplist.objects.get(writer=request.user, media_id=media).delete()
        return redirect('mypage:home', nickname)