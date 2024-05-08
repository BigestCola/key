# user/urls.py

from django.urls import path
from . import views
from .views import user_login, user_logout
from django.contrib.auth.views import LogoutView
from django.contrib import admin
from django.urls import path, include


app_name = 'user'

urlpatterns = [
    path('', views.home, name='user_home'),
    path('home/', views.user_home, name='user_home'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('create/', views.UserCreateView.as_view(), name='user_create'),
    path('update/<int:pk>/', views.UserUpdateView.as_view(), name='user_update'),
    path('generate_cdkey/', views.generate_cdkey, name='generate_cdkey'),
    path('cdkey_record/', views.cdkey_record, name='cdkey_record'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('subordinate/create/', views.subordinate_create, name='subordinate_create'),
    path('subordinate/<int:subordinate_id>/edit/', views.subordinate_edit, name='subordinate_edit'),
    path('subordinate/<int:subordinate_id>/delete/', views.subordinate_delete, name='subordinate_delete'),
    path('subordinate/<int:user_id>/cdkeys/', views.subordinate_cdkeys_view, name='subordinate_cdkeys'),
    path('subordinate/', views.subordinate_list, name='subordinate_list'),
    path('subordinate/<int:user_id>/cdkeys/monthly-summary/', views.subordinate_cdkeys_monthly_summary, name='subordinate_cdkeys_monthly_summary'),
    path('subordinate/<int:user_id>/cdkeys/custom-summary/', views.subordinate_cdkeys_custom_summary, name='subordinate_cdkeys_custom_summary'),
    path('cdkey/record/', views.cdkey_record, name='cdkey_record'),
    path('cdkey/monthly-summary/', views.cdkey_monthly_summary, name='cdkey_monthly_summary'),
    path('cdkey/custom-summary/', views.cdkey_custom_summary, name='cdkey_custom_summary'),
    path('subordinate/<int:subordinate_id>/cdkeys/', views.subordinate_cdkey_record, name='subordinate_cdkey_record'),
    path('subordinate/<int:subordinate_id>/cdkey_record/', views.subordinate_cdkey_record, name='subordinate_cdkey_record'),

]
