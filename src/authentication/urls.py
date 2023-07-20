from django.urls import path, re_path, include

from rest_framework_simplejwt.views import TokenVerifyView

from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.views import LoginView


app_name = "authentication"


api_v1_urls = [
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/refresh/", get_refresh_view().as_view(), name="token_refresh"),
    path("auth/verify/", TokenVerifyView.as_view(), name="token_verify"),
]

urlpatterns = [
    re_path('^api/(?P<version>(v1))/', include(api_v1_urls)),
]
