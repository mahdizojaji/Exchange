from rest_framework import generics, permissions

from ....models import User
from ....serializers import UserSerializer

class UserMixin:
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('-date_joined').prefetch_related('groups')
    permission_classes = [permissions.AllowAny]


class UserListAPIView(UserMixin, generics.ListAPIView):
    pass


class UserRetrieveAPIView(UserMixin, generics.RetrieveAPIView):
    lookup_field = 'uuid'
