import requests
from decouple import config
from django.conf import settings
from django.http import Http404
from rest_framework.response import Response

from api.v1.wallet.utils import login_to
from orders.models import CartModel
from wallet.models import WalletModel, TransferModel

EDUON_WALLET = config('EDUON_WALLET')

WALLET_URL = config('WALLET_URL')
HEADER = {"token": f"{settings.WALLET_TOKEN}"}


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


def proceed_transfer(wallet, total_price):
    # TODO: check if enough money
    # TODO: transfer from user wallet to EduOn
    payload = {
        "id": "{{$randomUUID}}",
        "method": "transfer.create",
        "params": {
            "number": f"{wallet.card_number}",
            "expire": f"{wallet.expire}",
            "receiver": f"{EDUON_WALLET}",
            "amount": f"{total_price}",
        }
    }
    try:
        response_data = requests.post(url=WALLET_URL, json=payload, headers={"token": f"{settings.WALLET_TOKEN}"})
    except:
        return Response({'message': 'Service is not working.'})

    if response_data.json()['status']:
        try:
            TransferModel.objects.create(
                wallet=wallet, tr_id=response_data.json()['result']['tr_id'],
                status=False, amount=total_price,
                sender="", type=False
            )
        except:
            return Response({'status': True, 'message': "TransferModel object create failed!", 'tr_id': response_data.json()['result']['tr_id']})

        return Response(response_data.json())
    elif response_data.json()['error']['code'] == '-15':
        return Response(response_data.json())
    elif response_data.json()['error']['code'] == '404':
        token = login_to()
        try:
            data = requests.post(url=WALLET_URL, json=payload, headers={"token": f"{token}"})
        except:
            return Response({'status': False, 'message': 'Service is not working.'})

        try:
            TransferModel.objects.create(
                wallet=wallet, tr_id=data.json()['result']['tr_id'],
                status=False, amount=total_price,
                destination=str(EDUON_WALLET), type=False
            )
        except:
            return Response({'status': True, 'message': "TransferModel object create failed!", 'tr_id': data.json()['result']['tr_id']})

        return Response(data.json())
    else:
        return Response(response_data.json())

    # TODO: transfer from EduOn to speaker
    # TODO: rollback in case of exception


