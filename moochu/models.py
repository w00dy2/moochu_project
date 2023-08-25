from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

from django.db import models
from django.utils import timezone
from django.conf import settings
from pymongo import MongoClient

# db 연결
mongo_client = MongoClient(settings.MONGODB_URL)

media_db= mongo_client[settings.ALL_MONGODB_NAME]

daum_db = mongo_client[settings.DAUM_MONGODB_NAME]

class Media:
    collection=media_db.movies2



