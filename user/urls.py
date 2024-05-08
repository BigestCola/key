# user/urls.py

from django.urls import path
from . import views
from .views import user_login, user_logout

urlpatterns = [
    path('list/', views.UserListView.as_view(), name='user_list'),
    path('create/', views.UserCreateView.as_view(), name='user_create'),
    path('update/<int:pk>/', views.UserUpdateView.as_view(), name='user_update'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('subordinate/', views.subordinate_list, name='subordinate_list'),
    path('subordinate/create/', views.subordinate_create, name='subordinate_create'),
    path('subordinate/<int:subordinate_id>/edit/', views.subordinate_edit, name='subordinate_edit'),
    path('subordinate/<int:subordinate_id>/delete/', views.subordinate_delete, name='subordinate_delete'),
    path('generate_cdkey/', views.generate_cdkey, name='generate_cdkey'),
]
