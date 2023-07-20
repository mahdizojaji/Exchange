from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from src.core.models import BaseModel


User = get_user_model()


class Order(BaseModel):
    class StatusChoices(models.TextChoices):
        INITIATED = 'initiated', _('Initiated')
        AWAITING_PAYMENT = 'awaiting-payment', _('Awaiting Payment')
        CANCEL = 'cancel', _('Cancel')
        AWAITING_AGGREGATING = 'awaiting-aggregating', _('Awaiting Aggregating')
        IN_PROGRESS = 'in-progress', _('In_Progress')
        DONE = 'done', _('Done')
        UNSUCCESSFUL = 'unsuccessful', _('Unsuccessful')


    class ActionChoices(models.TextChoices):
        BUY = 'buy', 'Buy'
        SELL = 'sell', 'Sell'
        TRANSFER = 'Transfer', 'Transfer'

    user = models.ForeignKey(
        verbose_name=_('User'),
        to=User,
        on_delete=models.CASCADE,
        related_name='orders',
    )
    status = models.CharField(
        verbose_name=_('Status'),
        max_length=255,
        choices=StatusChoices.choices,
        default=StatusChoices.INITIATED,
    )
    action = models.CharField(
        verbose_name=_('Type'),
        max_length=255,
        choices=ActionChoices.choices,
    )
    ref_id = models.CharField(
        verbose_name=_('RefID'),
        max_length=255,
        null=True,
        blank=True,
    )
    quantity = models.IntegerField(verbose_name=_("Quantity"))
    currency = models.ForeignKey(
        verbose_name=_('Currency'),
        to='exchange.Currency',
        on_delete=models.CASCADE,
        related_name='trades',
    )
    target = models.ForeignKey(
        verbose_name=_('Target'),
        to='exchange.Wallet',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='transfer_orders',
    )
    price = models.IntegerField(
        verbose_name=_('Price'),
        null=False,
        blank=False,
    )
    description = models.TextField(
        verbose_name=_('Description'),
        null=True,
        blank=True,
        default=None,
    )

    def __str__(self):
        return f'{self.uuid} -> {self.get_action_display()} {self.quantity} {self.currency} ({self.get_status_display()})'


    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
