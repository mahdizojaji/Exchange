from django.contrib import admin

from ..models import Wallet, Transaction


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    actions = ['recalculate']

    @admin.action(description='Recalculate')
    def recalculate(self, __, queryset):
        for obj in queryset:
            obj: Wallet
            obj.recalculate_balance()

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    actions = ['make_paid']

    @admin.action(description='Make Paid')
    def make_paid(self, __, queryset):
        queryset.update(status=Transaction.StatusChoices.PAID)
