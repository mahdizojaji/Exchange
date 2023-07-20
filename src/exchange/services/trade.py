from secrets import token_hex

from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.db.models.aggregates import Sum

from ..models import Order

def buy_crypto_currency(user, currency, quantity):
    with transaction.atomic():
        order_price = currency.price * quantity
        user.wallet.withdraw(order_price)
        order = create_initiated_order(user, currency, quantity, Order.ActionChoices.BUY)
        # TODO: maybe should do this in background
        ref_id, settlement_orders = make_settlement(order)
        update_order_status_via_settlement(ref_id, settlement_orders, order)
        order.save()

    return order


def create_initiated_order(user, currency, quantity, action):
    return Order.objects.create(
        user=user,
        status=Order.StatusChoices.INITIATED,
        action=action,
        currency=currency,
        price=currency.price * quantity,
        quantity=quantity,
    )


def make_settlement(order):
    if order.price >= settings.MINIMUM_ORDER_PRICE:
        return buy_from_exchange(order.currency, order.quantity), [order]
    elif aggregate_orders := find_orders_for_aggregate(order):
        print('hello')
        return (
            buy_from_exchange(order.currency, aggregate_orders.aggregate(Sum('quantity'))['quantity__sum']),
            aggregate_orders
        )
    else:
        return None, []


def update_order_status_via_settlement(ref_id, orders, current_order):
    if ref_id:
        for order in orders:
            print(order.id)
            order.status = Order.StatusChoices.IN_PROGRESS
            order.save()
    else:
        current_order.status = Order.StatusChoices.AWAITING_AGGREGATING
        current_order.save()


def find_orders_for_aggregate(order: Order):
    sum_price = Order.objects.filter(
        (Q(status=Order.StatusChoices.AWAITING_AGGREGATING) | Q(id=order.id)),
        currency=order.currency,
    ).aggregate(Sum('price'))['price__sum']
    print(sum_price)
    print(settings.MINIMUM_ORDER_PRICE)
    if sum_price > settings.MINIMUM_ORDER_PRICE:
        print(list(Order.objects.filter(
        Q(status=Order.StatusChoices.AWAITING_AGGREGATING) |
        Q(id=order.id, status=Order.StatusChoices.INITIATED),
        currency=order.currency,
        )))
        return Order.objects.filter(
        Q(status=Order.StatusChoices.AWAITING_AGGREGATING) |
        Q(id=order.id, status=Order.StatusChoices.INITIATED),
        currency=order.currency,
        )
    return []


def buy_from_exchange(currency, quantity):
    # TODO: Http request to international exchange
    return token_hex(10)
