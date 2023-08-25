from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm,GenreSelectForm
from .models import Genre,SelectedGenre,MovieRating, User
from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
import logging
from django.http import JsonResponse
from moochu.models import Media
import requests
logger=logging.getLogger('common')


def protected_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        next_page = request.POST.get('next')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({'success': True, 'next_page': next_page})
        else:
            return JsonResponse({'success': False, 'error': '로그인에 실패하였습니다.'})
        

    else:
        return render(request, 'common/protected.html')
    

## 회원가입 
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            current_site = get_current_site(request) 
            message = render_to_string('common/register_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_title = "계정 활성화 확인 이메일"
            mail_to = request.POST["email"]
            email = EmailMessage(mail_title, message, to=[mail_to])
            email.send()
            address = "http://www." + mail_to.split('@')[1]
            form = { "user": user,
                    "address": address }
            return render(request, 'common/register_complete.html', form)
    else:
        form = RegistrationForm()
    return render(request, 'common/register.html', {'form': form})

def register_complete(request):
    return render(request, 'common/register_complete.html')

## 로그인 함수
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        next_page = request.POST.get('next')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({'success': True, 'next_page': next_page})
        else:
            return JsonResponse({'success': False, 'error': '로그인에 실패하였습니다.'})
        

    else:
        return render(request, 'common/login.html', {'error': ''})

## 관심 장르 선택 함수
GENRE_CHOICES = {
    1: "SF",
    2: "가족",
    3: "공연",
    4: "공포(호러)",
    5: "다큐멘터리",
    6: "드라마",
    7: "멜로/로맨스",
    8: "뮤지컬",
    9: "미스터리",
    10: "범죄",
    11: "서부극(웨스턴)",
    12: "서사",
    13: "서스펜스",
    14: "성인",
    15: "스릴러",
    16: "시사/교양",
    17: "애니메이션",
    18: "액션",
    19: "어드벤처(모험)",
    20: "예능",
    21: "음악",
    22: "전쟁",
    23: "코미디",
    24: "키즈",
    25: "판타지"
    # 나머지 번호와 장르를 추가하세요.
}
def get_genre_name(genre_id):
    return GENRE_CHOICES.get(genre_id, 'Unknown')

def movie_selection(request):
    if request.method == 'POST': # post로 평점 매기면 저장하는 코드.
        user = request.user
        movies = Media.collection.find({})
        for movie in movies:
            movie_id = str(movie['_id'])
            rating_key = f"rating_{movie_id}"
            if rating_key in request.POST:
                media_id = movie["_id"]
                rating = request.POST[rating_key]

                # === FastAPI 필요한 부분 시작 ===
                data = {
                    "user_id": user.pk,
                    "media_id": movie_id,
                    "genre_id": ",".join(movie["genres"]),
                    "rating": float(rating),
                }
                response = requests.post("http://34.64.249.190:8001/user_info/", json=data)
                if response.status_code != 200:
                    # 에러 처리
                    print(f"Error posting data to FastAPI: {response.text}")

                # === FastAPI 필요한 부분 끝 ===
                else:
                    try:
                        # 변경된 부분: get_or_create를 사용해 중복 저장을 방지합니다.
                        movie_rating, created = MovieRating.objects.get_or_create(user=user, media_id=media_id, defaults={'rating': rating})

                        # 만약 이미 존재하는 평점이라면 이전에 저장된 결과를 업데이트합니다.
                        if not created:
                            movie_rating.rating = rating
                            movie_rating.save()

                    except ValidationError:
                        pass

        return redirect('moochu:main')
    else: # 처음에 post요청이 없을때 보여주는 용. 
        select_genres = SelectedGenre.objects.filter(user=request.user).values_list('genre', flat=True)  # 가져온 필드를 사용하여 장르를 선택
        select_genre_names = [get_genre_name(int(g)) for g in select_genres]  # 선택된 장르 번호를 이름으로 매핑
        # 수정할 부분: 선택한 장르와 관련된 영화
        pipeline = [
            {"$match": {"genres": {"$elemMatch": {"$in": select_genre_names}}, "indexRating.score": {"$gte": 73.2}}},
            {"$sample": {"size": 30}}  # 임시로 충분히 큰 숫자를 지정해 무작위 순서로 문서들을 반환받는다.
        ]

        movies = Media.collection.aggregate(pipeline)

        if request.user.is_authenticated:
            user_id = request.user.id
        else:
            user_id = None
        movie_str = []
        info_string='recommend_movie'
        for movie in movies:
            movie['m_id'] = str(movie['_id'])
            movie_str.append(movie)
            logger.info(f'{movie["m_id"]},{info_string}', extra={'user_id': user_id})

        return render(request, 'common/movie_selection.html', {'movies': movie_str})

def genre_selection(request):
    if request.method == 'POST':
        form = GenreSelectForm(request.POST)
        if form.is_valid():
            user = request.user
            selected_genres = form.cleaned_data.get('selected_genres')

            for genre in selected_genres: 
                selected_genre = SelectedGenre(user=user, genre=genre) 
                selected_genre.save()

            return redirect('common:movie_selection')
    else:
        form = GenreSelectForm()
        genres = Genre.objects.all()

        return render(request, 'common/genre_selection.html', {'form': form, 'genres': genres})

@login_required
def save_genre(request):
    all_genres = get_genre_name()

    if request.method == 'POST':
      form = GenreSelectForm(request.POST, genre_choices=all_genres)
      if form.is_valid():
            selected_genres = form.cleaned_data['selected_genres']
            for genre_choice_id in selected_genres:
                choice_text = form.fields['selected_genres'].choices_dict.get(genre_choice_id)
                selected_genre = SelectedGenre(genre=choice_text)
                selected_genre.save()
                print(f'장르 저장 완료: {choice_text}')  
            return render(request, 'common/genre_selection.html')
    else:
        form = GenreSelectForm(genre_choices=all_genres)

    return render(request, 'common/genre_selection.html', {'form': form})


# 계정 활성화 함수(토큰을 통해 인증)
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return redirect("common:authentication")
    
def authentication(request):
    return render(request, 'common/Authentication_complete.html')