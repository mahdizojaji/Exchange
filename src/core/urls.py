from django.urls import re_path, path, include

from .views.api.v1.user import (
    UserListAPIView, UserRetrieveAPIView, UserDetailsRetrieveUpdateAPIView
)

app_name = 'core'

api_v1_urls = [
    path('users/', UserListAPIView.as_view(), name='UserListAPI-v1'),
    path('users/details/', UserDetailsRetrieveUpdateAPIView.as_view(), name='UserDetailsAPI-v1'),
    path('users/<uuid:uuid>/', UserRetrieveAPIView.as_view(), name='UserRetrieveAPI-v1'),
]

urlpatterns = [
    re_path('^api/(?P<version>(v1))/', include(api_v1_urls)),
]
