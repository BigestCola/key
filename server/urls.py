# server/urls.py

from django.contrib import admin
from django.urls import path, include
from user.views import home, user_login  # 导入 home 和 user_login 视图函数

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', user_login, name='login'),  # 直接使用 user_login
    path('user/', include('user.urls')),
    path('cdkey/', include('cdkey.urls')),
]