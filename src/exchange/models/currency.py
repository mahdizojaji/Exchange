from django.db import models
from django.utils.translation import gettext_lazy as _

from src.core.models import BaseModel


class Currency(BaseModel):
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=50,
        unique=True,
    )
    symbol = models.CharField(
        verbose_name=_('Symbol'),
        max_length=10,
        unique=True,
        db_index=True,
    )
    price = models.DecimalField(
        verbose_name=_('Price'),
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')
