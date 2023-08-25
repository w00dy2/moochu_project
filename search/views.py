from django.shortcuts import render, redirect

# Create your views here.
from rest_framework.views import APIView  
from rest_framework.response import Response  
from rest_framework import status  
from elasticsearch import Elasticsearch  
from moochu.models import Media
from collections import OrderedDict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import redis
import logging
import connection

logger=logging.getLogger('search')
  
def trans(hits):
    hits_list=[]
    for hit in hits:
        hits_list.append(hit['_source'])

    return hits_list[:12]


class SearchView(APIView):
    def get(self, request):
        es = Elasticsearch([connection.elastic_bulk])

        search_word = request.GET.get('search')
        if request.user.is_authenticated:
            user_id = request.user.id
        else:
            user_id = None
        info_string='search'
        logger.info(f'{search_word},{info_string}', extra={'user_id': user_id})

        if not search_word:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'search word param is missing'})

        docs = es.search(
            index='media3',
            body={
                "query": {
                    "multi_match": {
                        "query": search_word,
                        "fields": ["id","title"]                    
                    }
                }
            }
        )

        data_list = trans(docs['hits']['hits'])


        # Redis 클라이언트 생성
        r = redis.StrictRedis(connection.redis_r0)

        search = r.zrevrange('search', 0, 11, withscores=True)

        # ByteArray를 디코드하여 문자열로 변환
        search = [(item[0].decode('utf-8'), item[1]) for item in search]
        search = [x[0] for x in search]
        top5 = search[:5]
        top10 = search[5:10]

        if data_list:
            context = {
            'data': data_list,
            'top5': top5,
            'top10': top10,
            }

            
            return render(request, 'search/result.html',context)
        else:
            context = {
            'top5': top5,
            'top10': top10,
            }
            return render(request, 'search/result.html',context)

def data_change(request,data):
    data =[
        {
            'id': str(movie['_id']),
            'posterImageUrl': movie['poster_image_url'],
            'title': movie['title_kr'],
        }
        for movie in data
    ]

    paginator = Paginator(data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj

def search(request):
    pipeline = [
            {"$match": {"media_type": "MOVIE","indexRating.score": {"$gte": 95}}},
            {"$sample": {"size": 1000}}  # 임시로 충분히 큰 숫자를 지정해 무작위 순서로 문서들을 반환받는다.
        ]

    data = Media.collection.aggregate(pipeline)

    

    page_obj= data_change(request,data)


    # Redis 클라이언트 생성
    r = redis.StrictRedis(connection.redis_r0)

    search = r.zrevrange('search', 0, -1, withscores=True)

    # ByteArray를 디코드하여 문자열로 변환
    search = [(item[0].decode('utf-8'), item[1]) for item in search]
    search = [x[0] for x in search]
    top5 = search[:5]
    top10 = search[5:10]
    context = {
        'data': page_obj,
        'top5': top5,
        'top10': top10,
    }

    return render(request, 'search/home.html', context)
