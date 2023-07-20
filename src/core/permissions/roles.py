from django.contrib.auth import get_user_model

from rest_framework.permissions import BasePermission

User = get_user_model()


class IsSelfOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if isinstance(obj, User) and obj == request.user:
            return True

        return False
