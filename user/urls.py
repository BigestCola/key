# user/urls.py

from django.urls import path
from . import views
from .views import user_login, user_logout

app_name = 'user'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.change_password, name='change_password'),
    path('generate-cdkey/', views.generate_cdkey, name='generate_cdkey'),
    path('cdkey-records/', views.cdkey_records, name='cdkey_records'),
    path('create/', views.user_create, name='user_create'),
    path('update/int:pk/', views.UserUpdateView, name='user_update'),
    path('delete/int:pk/', views.user_delete, name='user_delete'),

]
