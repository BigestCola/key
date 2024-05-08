# server/urls.py

from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required
from user import views
from user.views import UserViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('login/', views.user_login, name='login'),
    path('', views.user_home, name='user_home'),
    path('', UserViews.as_view(user_home), name='user_home'),
]