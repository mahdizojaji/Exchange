from .base import BaseManager
from django.contrib.auth.models import UserManager as _UserManager


class UserManager(_UserManager, BaseManager):
    pass
