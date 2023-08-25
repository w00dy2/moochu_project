from pathlib import Path
import os
from django.conf import settings
import connection 


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

AUTH_USER_MODEL = 'common.User'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = connection.secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "common",
    "board",
    "moochu",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "rest_framework",
    "mypage",
    "search",
    "review",

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 'config.middleware.LoginRequiredMiddleware', # 동영상 로그인 페이지 통해서만 홈페이지 이용가능
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'), 
            os.path.join(BASE_DIR, 'templates', 'accounts')
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
AUTH_USER_MODEL = 'common.User'


DATABASES = connection.mysqldb

ELASTICSEARCH_DSL = connection.elastic
#mongodb 설정
MONGODB_URL = connection.mongodb  # 데이터베이스의 MongoDB URI를 입력해주세요.
ALL_MONGODB_NAME = 'final'  # db 이름



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'movie_verbose': { # render한 영화에 대한 로그
            'format': '{levelname},{asctime},{user_id},{message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'user_action': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'user_action.log',
            'formatter': 'movie_verbose',
            'maxBytes': 1024*1024*10,
            'backupCount': 10,
        },
        'renderMovie': { 
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'renderMV.log',  
            'formatter': 'movie_verbose',
            'maxBytes': 1024*1024*10,
            'backupCount': 10, #초과한 용량의 로그파일을 백업할 횟수
        },
        'other_action': { 
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'renderMV.log',  
            'formatter': 'movie_verbose',
            'maxBytes': 1024*1024*10,
            'backupCount': 10, #초과한 용량의 로그파일을 백업할 횟수
        },
    },
    'loggers': {
        'moochu': {
            'handlers': ['user_action'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'board': {
            'handlers': ['other_action'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'mypage': {
            'handlers': ['other_action'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'review': {
            'handlers': ['user_action'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'search': {
            'handlers': ['user_action'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}


LANGUAGE_CODE = "ko-kr"

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True



STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# 장고디비에 이미지 파일올리기

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


LOGIN_REDIRECT_URL = "/moochu"
LOGOUT_REDIRECT_URL = ""
ACCOUNT_LOGOUT_ON_GET = True

# 기본 프로필 이미지 경로 설정
DEFAULT_PROFILE_IMAGE = 'media/profiles/chuchu.png'  # 기본 이미지 파일의 경로

# Email sending

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
# 메일을 호스트하는 서버
EMAIL_PORT = '587'
# gmail과의 통신하는 포트
EMAIL_HOST_USER = connection.email_user
# 발신할 이메일
EMAIL_HOST_PASSWORD = connection.email_pass
# 발신할 메일의 비밀번호
EMAIL_USE_TLS = True
# TLS 보안 방법
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER








