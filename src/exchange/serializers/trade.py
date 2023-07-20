from rest_framework import serializers

from ..models import Order
from ..exeptions import InvalidTradeAction
from ..services.trade import buy_crypto_currency


class TradeCryptoCurrencySerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)

    def create(self, validated_data):
        request = self.context['request']
        action = self.context['action']
        currency = self.context['currency']
        quantity = validated_data['quantity']

        if action == 'BUY':
            return buy_crypto_currency(request.user, currency, quantity)
        elif action == 'SELL':
            ...
        elif action == 'TRANSFER':
            ...
        else:
            raise InvalidTradeAction('Trade action is invalid.')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'