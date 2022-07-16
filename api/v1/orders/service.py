from django.http import Http404

from orders.models import CartModel
from wallet.models import WalletModel


# Payment service methods
def get_wallet(account):
    try:
        return WalletModel.objects.get(owner=account)
    except WalletModel.DoesNotExist:
        raise Http404


def get_cart_items(account):
    try:
        cart_items = CartModel.objects.filter(owner=account)
        return cart_items
    except CartModel.DoesNotExist:
        raise Http404


def get_cart_total_price(account):
    total_price = 0

    cart_items = get_cart_items(account)

    for i in range(len(cart_items)):
        total_price += cart_items[i].course.price
    return total_price


def proceed(cart_items, status):
    if not status:
        return False

    # cart_items =


def proceed_transfer(wallet):
    # TODO: check if enough money
    # TODO: transfer from user wallet to EduOn
    # TODO: transfer from EduOn to speaker
    # TODO: rollback in case of exception


    pass

