from django.db import models
from django.db.models.manager import BaseManager as _BaseManager


class BaseQuerySet(models.QuerySet):
    pass


class BaseManager(_BaseManager.from_queryset(BaseQuerySet)):
    pass
