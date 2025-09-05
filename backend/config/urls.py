from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.permissions import AllowAny
from django.urls import path

obtain_auth_token.permission_classes = [AllowAny]

urlpatterns = [
    path('api/token', obtain_auth_token, name='api_token_auth'),
]
