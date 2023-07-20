from django.urls import re_path, path, include


from .views.api.v1 import CurrencyBuyAPIView, CurrencySellAPIView, CurrencyTransferAPIView


app_name = 'exchange'

api_v1_urls = [
    path('currency/<str:symbol>/buy/', CurrencyBuyAPIView.as_view(), name='ExchangeTradeAPI-v1'),
    path('currency/<str:symbol>/sell/', CurrencySellAPIView.as_view(), name='ExchangeTradeAPI-v1'),
    path('currency/<str:symbol>/transfer/', CurrencyTransferAPIView.as_view(), name='ExchangeTradeAPI-v1'),
]

urlpatterns = [
    re_path('^api/(?P<version>(v1))/', include(api_v1_urls)),
]
