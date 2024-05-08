# server/urls.py

from django.contrib import admin
from django.urls import path, include
from .views import home
from django.urls import path, include
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/cdkey/', include('cdkey.urls')),
    path('api/user/', include('user.urls')),
    path('', include(('user.urls', 'user'), namespace='user')),
    path('', views.home, name='home'),
]