from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from bson import ObjectId
from django.db.models import Avg
from common.models import MovieRating
from review.models import Review
from .models import Media
from collections import OrderedDict
import redis
import re
import random
from datetime import datetime
from collections import defaultdict
import logging
import connection

logger=logging.getLogger('moochu')
# Create your views here.
def convert_to_movie_dict(media_data):
    return {
        'id': str(media_data["_id"]),
        'title': media_data["title_kr"]
    }

# 페이징을 위한 호출 함수
def data_change(request,data):
    data =[
        {
            'id': str(movie['_id']),
            'posterImageUrl': movie['poster_image_url'],
            'titleKr': movie['title_kr'],
        }
        for movie in data
    ]

    paginator = Paginator(data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj


## mainpage 함수
def mainpage(request):

    # Redis 클라이언트 생성
    r0 = redis.StrictRedis(connection.redis)

    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        user_id = None
    info_string='main'
    logger.info(f'moochu,{info_string}', extra={'user_id': user_id})

                                                  ## 오늘의 영화 TOP10 데이터 
    # Redis에서 'popularity'에 해당하는 값을 가져옴
    value = r0.zrevrange('popularity', 0, -1, withscores=True)

    # ByteArray를 디코드하여 문자열로 변환
    value = [(item[0].decode('utf-8'), item[1]) for item in value]

    # 첫 번째 값만 다른 변수에 저장
    top1 = list(value[0])
    top1_data = Media.collection.find_one({'_id': ObjectId(top1[0])})
    top1_reviews = Review.objects.filter(media_id=str(top1_data['_id'])).order_by('-create_date')
    top1_review = top1_reviews.first()


    top1 ={
            'id': str(top1_data['_id']),
            'title': top1_data['title_kr'],
            'synopsis': top1_data['synopsis'],
        }
    

    # 나머지 값들은 value에 저장
    ranking = value[1:10]
    top2=[]

    for media in ranking:
        media = list(media)
        top2_data = Media.collection.find_one({'_id': ObjectId(media[0])})
        top2_data ={
            'id':str(top2_data['_id']),
            'title': top2_data['title_kr'],
            'synopsis': top2_data['synopsis']
        }
        
        top2.append(top2_data)
    
                                                ## 최신 리뷰 데이터 들고오기 
    reviews = Review.objects.order_by('-create_date')
    review_count = reviews.count()
    combined_data = []

    for review in reviews:
        media_id = review.media_id
        media_data = Media.collection.find_one({'_id': ObjectId(media_id)})
        movie = convert_to_movie_dict(media_data)
        if movie is not None:  # Check if movie is not None before appending to the list
            combined_review_movie_data = {
                'movie': movie,
                'review': review,
            }

            combined_data.append(combined_review_movie_data)
                         ## 최근 본 미디어 데이터 
    
    value = r0.lrange(str(request.user.id), 0, 10)

    value = [(item.decode('utf-8')) for item in value]

    recent=[]
    try:
        for media in value:
            recent_data = Media.collection.find_one({'_id': ObjectId(media)})
            recent_data ={
                'id': str(recent_data['_id']),
                'title': recent_data['title_kr'],
                'synopsis': recent_data['synopsis']
            }
            
            recent.append(recent_data)
    except:
        pass

                                                ## 추천 결과 미디어 랜덤으로 20개 
    try:
        r3 = redis.StrictRedis(connection.redis_r1)
        if r3.lrange(str(request.user.id), 1, 100):
            value = r3.lrange(str(request.user.id), 1, 100)
        else:
            r2 = redis.StrictRedis(connection.redis_r2)
            value = r2.lrange(str(request.user.id), 1, 100)


        # 랜덤하게 20개 선택
        items = random.sample(value, 20)
        recommendation = [(item.decode('utf-8')) for item in items]
    except:
        recommendation= None

                                                ## 인기 영화 20개 
    pipeline = [
            {"$match": {"media_type": "MOVIE","indexRating.score": {"$gte": 99}}},
            {"$sample": {"size": 1000}}  # 임시로 충분히 큰 숫자를 지정해 무작위 순서로 문서들을 반환받는다.
        ]

    recommendation_data = Media.collection.aggregate(pipeline)

    

    page_obj= data_change(request,recommendation_data)

    

    context = {
        "top1": top1,
        "top2": top2, 
        "reviews": reviews,
        'top1_review':top1_review,
        'combined_data':combined_data,
        'recent': recent,
        'recommendation':recommendation,
        'popu' : page_obj,
        'review_count':review_count,
    }
    
    
    return render(request, 'moochu/mainpage.html', context)
    




# 페이징을 위한 호출 함수
def data_change(request,data):
    data =[
        {
            'id': str(movie['_id']),
            'posterImageUrl': movie['poster_image_url'],
            'titleKr': movie['title_kr'],
        }
        for movie in data
    ]

    paginator = Paginator(data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj


def ott_media_list(request, ott, media_type):
    ott_service = ['All', 'Netflix', 'Tving', 'Watcha', 'Coupang', 'Wavve', 'Disney', 'Apple', 'Google', 'Laftel', 'Serieson', 'Primevideo', 'UPlus', 'CineFox']

    genres=['SF', '가족', '공연', '공포(호러)', '다큐멘터리', '드라마', '멜로/로맨스', '뮤지컬', '미스터리', '범죄',
                   '서부극(웨스턴)', '서사', '서스펜스', '성인', '스릴러', '시사/교양', '애니메이션', '액션', '어드벤처(모험)',
                   '예능', '음악', '전쟁', '코미디', '키즈', '판타지']
    
    if ott=='All':
        pipeline = [
            {"$match": {"media_type": media_type, "indexRating.score": {"$gte": 73.2}}},
            {"$sample": {"size": 1000}} 
        ]

        data = Media.collection.aggregate(pipeline)

    else:
        pipeline = [
            {"$match": {"media_type": media_type, "OTT": {"$in": [ott]}, "indexRating.score": {"$gte": 73.2}}},
            {"$sample": {"size": 1000}}
        ]
        data = Media.collection.aggregate(pipeline)


    
    page_obj= data_change(request,data)

    context = {
        'ott': ott,
        'data': page_obj,
        'genres' : genres,
        'type':media_type,
        'ott_service':ott_service
    }
    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        user_id=0
    info_string='media_list'
    logger.info(f'moochu,{info_string}', extra={'user_id': user_id})
    return render(request, 'moochu/movie_list.html', context)


def genre_filter(request, ott, media_type):
    ott_service = ['All', 'Netflix', 'Tving', 'Watcha', 'Coupang', 'Wavve', 'Disney', 'Apple', 'Google', 'Laftel', 'Serieson', 'Primevideo', 'UPlus', 'CineFox']

    genres=['SF', '가족', '공연', '공포(호러)', '다큐멘터리', '드라마', '멜로/로맨스', '뮤지컬', '미스터리', '범죄',
                   '서부극(웨스턴)', '서사', '서스펜스', '성인', '스릴러', '시사/교양', '애니메이션', '액션', '어드벤처(모험)',
                   '예능', '음악', '전쟁', '코미디', '키즈', '판타지']
    
    selected_genres = request.GET.getlist('genres')
    if not selected_genres:
        return redirect('moochu:ott_media_list', media_type=media_type, ott=ott)
    if ott=='All':
        pipeline = [
            {"$match": {"genres": {"$elemMatch": {"$in": selected_genres}}, "indexRating.score": {"$gte": 73.2}}},
            {"$sample": {"size": 1000}}  
        ]


        data = Media.collection.aggregate(pipeline)
        
    else:
        pipeline = [
            {"$match": {"genres": {"$elemMatch": {"$in": selected_genres}}, "indexRating.score": {"$gte": 73.2}}},
            {"$sample": {"size": 1000}} 
        ]


        data = Media.collection.aggregate(pipeline)

    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        user_id=0
    info_string='media_list'
    logger.info(f'moochu,{info_string}', extra={'user_id': user_id})


    page_obj= data_change(request,data)

    context = {
        'ott': ott,
        'data': page_obj,
        'genres' : genres,
        'selected_genres': selected_genres,
        'type':media_type,
        'ott_service':ott_service
    }

    return render(request, 'moochu/movie_list.html', context)




# 영화 상세 페이지 
def movie_detail(request, movie_id):
    data = list(Media.collection.find({"_id": ObjectId(movie_id)}))
    data =[
        {
            'id': str(movie['_id']),
            'posterImageUrl': movie['poster_image_url'],
            'titleKr': movie['title_kr'],
            'age' : movie['rating'],
            'genre' : movie['genres'],
            'synopsis' : movie['synopsis'],
            'date' : movie['released_At'],
        }
        for movie in data
    ]
    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        user_id=0
    info_string='movie_detail'
    logger.info(f'{data[0]["id"]},{info_string}', extra={'user_id': user_id})

    average_rating = MovieRating.objects.filter(media_id=str(movie_id)).aggregate(Avg('rating'))['rating__avg']
    reviews = Review.objects.filter(media_id=str(movie_id)).order_by('-create_date')
    review_count = Review.objects.filter(media_id=str(movie_id)).count()

    if request.user.is_authenticated:
        user_review = Review.objects.filter(media_id=str(movie_id), writer=request.user).first()
    else:
        user_review = None

    context = {
            'movie': data[0],
            'average_rating': average_rating,
            'reviews': reviews,
            'review_count': review_count,
            'user_review': user_review,
            'movie_id': movie_id,
        }

    return render(request, 'moochu/media_detail.html', context)





def coming_next(request):    
    data = list(Media.collection.find({"coming": "TRUE"}, {"_id": 1, "poster_image_url": 1, "title_kr": 1, "released_At": 1, "OTT": 1}))
    today = datetime.today().date()

    
    # Dday 정렬하기
    grouped_movies = defaultdict(list)
    for movie in data:
        release_date = movie.get('released_At')
        if release_date and '-' in release_date:
            date_format = "%Y-%m-%d"  
            try:
                release_date = datetime.strptime(release_date, date_format).date()
            except ValueError:
                continue
            
            d_day = (release_date - today).days
            
            if d_day < 0 or d_day > 14:  # 14일 기준으로 보여줌
                continue
            
            movie['Dday'] = d_day
            movie['id'] = str(movie.pop('_id'))  # _id to id
            grouped_movies[d_day].append(movie)
    
    # 같은 제목의 경우 ott 추가 및 제외
    for day, movies in grouped_movies.items():
        deduplicated_movies = []
        merged_ott = defaultdict(list)
        movie_titles = {}
        
        for movie in movies:
            key = (re.sub(r'[^\w\s]', '', movie['title_kr']).replace(' ', ''), movie['released_At']) # 정제된 title_kr 값을 사용, 공백 삭제
            movie_titles[key] = movie
            ott = movie['OTT']
            if isinstance(ott, str):
                ott = [ott]
            elif not isinstance(ott, list):
                continue
            merged_ott[key].extend(ott)
            
        for key, movie in movie_titles.items():
            movie['OTT'] = list(set(merged_ott[key]))
            deduplicated_movies.append(movie)
    
    

        deduplicated_movies = sorted(deduplicated_movies, key=lambda x: x['Dday'], reverse=True)
   
        grouped_movies[day] = deduplicated_movies
    
    sorted_groups = sorted(grouped_movies.items(), key=lambda x: x[0])
    return render(request, 'moochu/coming_next.html', {'sorted_groups': sorted_groups})