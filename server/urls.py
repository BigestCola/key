# server/urls.py

from django.contrib import admin
from django.urls import path, include
from user.views import home  # 直接导入 home 视图函数

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # 使用 home 视图函数
    path('user/', include('user.urls')),
]