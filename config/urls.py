"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from allauth.account.views import ConfirmEmailView
from django.conf.urls.static import static
from django.conf import settings
from common.views import protected_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('common/', include('common.urls', namespace='common')),
    path('moochu/', include('moochu.urls', namespace='moochu')),  
    path('accounts/', include('allauth.urls')),
    path('accounts/confirm-email/<str:key>/', ConfirmEmailView.as_view(), name='account_confirm_email'),
    path('mypage/', include('mypage.urls', namespace='mypage')), 
    path('board/', include('board.urls', namespace='board')),  
    path('search/', include('search.urls', namespace='search')), 
    path('review/', include('review.urls', namespace='review')), 
    path('',protected_view, name='protected')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
