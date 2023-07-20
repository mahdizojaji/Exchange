from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated

from dj_rest_auth.views import UserDetailsView

from ....models import User
from ....permissions import IsSelfOrAdmin
from ....serializers import UserSerializer

class UserMixin:
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('-date_joined').prefetch_related('groups')


class UserListAPIView(UserMixin, generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]


class UserRetrieveAPIView(UserMixin, generics.RetrieveAPIView):
    lookup_field = 'uuid'
    permission_classes = [IsAuthenticated, IsSelfOrAdmin]


class UserDetailsRetrieveUpdateAPIView(UserDetailsView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSelfOrAdmin]
