# cdkey/urls.py

from django.urls import path
from .views import CDKeyQueryView, CDKeyGenerateView, CDKeyExtractView, CDKeyVerifyView

urlpatterns = [
    path('', CDKeyQueryView.as_view(), name='cdkey_query'),
    path('generate/', CDKeyGenerateView.as_view(), name='cdkey_generate'),
    path('extract/', CDKeyExtractView.as_view(), name='cdkey_extract'),
    path('verify/', CDKeyVerifyView.as_view(), name='cdkey_verify'),
]