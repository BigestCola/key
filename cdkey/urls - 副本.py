# cdkey/urls.py

from django.urls import path
from .views import CDKeyQueryView, CDKeyGenerateView, CDKeyExtractView, CDKeyVerifyView

urlpatterns = [
    path('cdkey/', CDKeyQueryView.as_view(), name='cdkey_query'),
    path('cdkey/generate/', CDKeyGenerateView.as_view(), name='cdkey_generate'),
    path('cdkey/extract/', CDKeyExtractView.as_view(), name='cdkey_extract'),
    path('cdkey/verify/', CDKeyVerifyView.as_view(), name='cdkey_verify'),
]