from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from ....models import Currency
from ....serializers import TradeCryptoCurrencySerializer, OrderSerializer


class CurrencyTradeMixin:
    queryset = Currency.objects.all()
    lookup_field = 'symbol'
    permission_classes = [IsAuthenticated]

    # noinspection PyPep8Naming
    @property
    def ACTION(self):
        raise NotImplemented

    def get_serializer_context(self):
        # noinspection PyUnresolvedReferences
        context = super().get_serializer_context()
        # noinspection PyUnresolvedReferences
        context.update({
            'action': self.ACTION,
            'symbol': self.kwargs['symbol'],
            'currency': self.get_object(),
            'request': self.request,
        })
        return context


    def post(self, request, *args, **kwargs):
        # noinspection PyUnresolvedReferences
        serializer = TradeCryptoCurrencySerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = OrderSerializer(instance=serializer.instance, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CurrencyBuyAPIView(CurrencyTradeMixin, generics.GenericAPIView):
    ACTION = 'BUY'


class CurrencySellAPIView(CurrencyTradeMixin, generics.GenericAPIView):
    ACTION = 'SELL'


class CurrencyTransferAPIView(CurrencyTradeMixin, generics.GenericAPIView):
    ACTION = 'SELL'
