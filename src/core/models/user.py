from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from . import BaseModel
from ..managers import UserManager


class User(AbstractUser, BaseModel):
    objects = UserManager()

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
