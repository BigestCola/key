# server/urls.py

from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls', namespace='user')),
    path('', login_required(views.home), name='user_home'),
]