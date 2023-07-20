from django.utils import timezone
from django.db import models, transaction
from django.db.models.aggregates import Sum
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from src.core.models import BaseModel

from ..exeptions import InsufficientBalance


User = get_user_model()

class Wallet(BaseModel):
    user = models.OneToOneField(
        verbose_name=_('User'),
        to=User,
        on_delete=models.CASCADE,
        related_name='wallet',
    )
    balance = models.DecimalField(
        verbose_name=_('Balance'),
        max_digits=100,
        decimal_places=4,
        default=0,
    )
    is_blocked = models.BooleanField(
        verbose_name=_('Block Status'),
        default=False,
    )

    def deposit(self, value):
        with transaction.atomic():
            wallet = Wallet.objects.select_for_update(nowait=True).only('balance').get(pk=self.pk)
            tr: Transaction = wallet.transactions.create(
                value=value,
                running_balance=wallet.balance + value,
                type=Transaction.TypeChoices.DEPOSIT,
            )

            wallet.balance += value
            tr.status = Transaction.StatusChoices.PAID
            tr.paid_date = timezone.now()

            tr.save()
            wallet.save()
            return wallet

    def withdraw(self, value):
        with transaction.atomic():
            wallet = Wallet.objects.select_for_update(nowait=True).only('balance').get(pk=self.pk)

            if value > wallet.balance:
                raise InsufficientBalance('This wallet has insufficient balance.')

            tr: Transaction = wallet.transactions.create(
                value=-value,
                running_balance=wallet.balance - value,
                type=Transaction.TypeChoices.WITHDRAW,
            )

            wallet.balance -= value
            tr.status = Transaction.StatusChoices.PAID
            tr.paid_date = timezone.now()

            tr.save()
            wallet.save()
            return wallet

    def recalculate_balance(self):
        with transaction.atomic():
            wallet = Wallet.objects.select_for_update().only('balance').get(pk=self.pk)
            sum_paid_transactions = self.transactions.filter(
                status=Transaction.StatusChoices.PAID
            ).aggregate(sum_value=Sum('value', default=0))['sum_value']
            wallet.balance = sum_paid_transactions
            wallet.save()

    def __str__(self):
        return '{} ( {:,.2f} )'.format(self.user, self.balance)

    class Meta:
        verbose_name = _('Wallet')
        verbose_name_plural = _('Wallets')


class Transaction(models.Model):
    class FeePayerChoices(models.TextChoices):
        SYSTEM = 'system', _('System')
        CUSTOMER = 'customer', _('Customer')

    class StatusChoices(models.TextChoices):
        INITIATED = 'initiated', _('Initiated')
        PAID = 'paid', _('Paid')
        CANCELED = 'canceled', _('Canceled')
        REJECTED = 'rejected', _('Rejected')
        EXPIRED = 'expired', _('Expired')

    class TypeChoices(models.TextChoices):
        WITHDRAW = 'withdraw', _('Withdraw')
        DEPOSIT = 'deposit', _('Deposit')

    wallet = models.ForeignKey(
        verbose_name=_('Wallet'),
        to=Wallet,
        on_delete=models.CASCADE,
        related_name='transactions',
    )
    value = models.DecimalField(
        verbose_name=_('Value'),
        max_digits=100,
        decimal_places=4,
    )
    fee = models.DecimalField(
        verbose_name=_('Fee'),
        max_digits=100,
        decimal_places=4,
        default=0,
    )
    fee_payer = models.CharField(
        verbose_name=_('Fee Payer'),
        max_length=255,
        choices=FeePayerChoices.choices,
        default=FeePayerChoices.CUSTOMER,
    )
    running_balance = models.DecimalField(
        verbose_name=_('Running Balance'),
        max_digits=100,
        decimal_places=4,
    )
    status = models.CharField(
        verbose_name='Payment Status',
        max_length=255,
        choices=StatusChoices.choices,
        default=StatusChoices.INITIATED,
    )
    type = models.CharField(
        verbose_name='Type',
        max_length=255,
        choices=TypeChoices.choices,
    )
    paid_date = models.DateTimeField(
        verbose_name='Paid DateTime',
        null=True,
        blank=True,
        default=None,
    )

    def __str__(self):
        return f'{self.get_type_display()} {self.value} ( {self.get_status_display()} ) -> {self.wallet}'

    class Meta:
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')
