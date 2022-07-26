import os

import requests
from decouple import config

# from eduon_v1 import settings
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response

from wallet.models import TransferModel

WALLET_URL = config('WALLET_URL')

LOGIN_USERNAME = config('LOGIN_USERNAME')
LOGIN_PASSWORD = config('LOGIN_PASSWORD')


def register_transfer(wallet, data):
    try:
        TransferModel.objects.create(
            wallet=wallet, tr_id=data['result']['tr_id'],
            amount=data['amount'], type=True,
            destination=data['number'], status=False
        )
    except:
        return Response({'status': True, 'message': "TransferModel object create failed!",
                         'tr_id': data['result']['tr_id']})


def login_to():
    payload = {
        "jsonrpc": "2.0",
        "id": "{{$randomUUID}}",
        "method": "partner.login",
        "params": {
            "username": f"{LOGIN_USERNAME}",
            "password": f"{LOGIN_PASSWORD}"
        }
    }
    token = settings.WALLET_TOKEN
    try:
        data = requests.post(url=WALLET_URL, json=payload)
        token = data.json()['result']['access_token']
        os.environ['WALLET_TOKEN'] = token
        settings.WALLET_TOKEN = token
    except:
        return {"status": False}

    return token


def create_wallet_util(phone_number):
    header = {"token": f"{settings.WALLET_TOKEN}"}
    payload = {
        "id": "{{$randomUUID}}",
        "method": "wallet.create",
        "params": {
            "name": "Test card",
            "phone": f"{phone_number}",
            "wallet_name": f"EduOn {phone_number}-card"
        }
    }
    try:
        data = requests.post(url=WALLET_URL, json=payload, headers={"token": f"{settings.WALLET_TOKEN}"})
    except:
        return {"status": False}

    if data.json()['status']:
        return Response(data.json())
    else:
        token = login_to()
        try:
            data = requests.post(url=WALLET_URL, json=payload, headers={"token": f"{token}"})

            if not data.json()['status']:
                return {'result': {'card_number': '0000', 'expire': '0000'}}

        except:
            return {'result': {'card_number': '0000', 'expire': '0000'}}
        return data.json()


def withdraw_from_wallet_service(wallet, data):
    payload = {
        "id": "{{$randomUUID}}",
        "method": "transfer.create",
        "params": {
            "number": f"{wallet.card_number}",
            "expire": f"{wallet.expire}",
            "receiver": f"{data['number']}",
            "amount": f"{data['amount']}",
        }
    }
    try:
        resp_data = requests.post(url=WALLET_URL, json=payload, headers={"token": f"{settings.WALLET_TOKEN}"})
    except:
        return Response(status.HTTP_404_NOT_FOUND)

    if resp_data.json()['status']:
        resp_data = resp_data.json()
        try:
            TransferModel.objects.create(
                wallet=wallet, tr_id=resp_data['result']['tr_id'],
                amount=data['amount'], type=True,
                destination=data['number'], status=False
            )
        except:
            return Response({'status': True, 'message': "TransferModel object create failed!", 'tr_id': resp_data['result']['tr_id']})
        return Response(resp_data)
    else:
        token = login_to()
        try:
            resp_data = requests.post(url=WALLET_URL, json=payload, headers={"token": f"{token}"})
        except:
            return Response({'message': 'Service is not working.'})

        try:
            TransferModel.objects.create(
                wallet=wallet, tr_id=resp_data.json()['result']['tr_id'],
                status=False, amount=data['amount'],
                destination=data['number'], type=False
            )
        except:
            return Response({'status': True, 'message': "TransferModel object create failed!",
                             'tr_id': resp_data.json()['result']['tr_id']})
        return Response(resp_data.json())


def transfer_service(wallet, data):
    payload = {
        "id": "{{$randomUUID}}",
        "method": "transfer.create",
        "params": {
            "number": f"{data['number']}",
            "expire": f"{data['expire']}",
            "receiver": f"{wallet.card_number}",
            "amount": f"{data['amount']}",
        }
    }

    try:
        resp_data = requests.post(url=WALLET_URL, json=payload, headers={"token": f"{settings.WALLET_TOKEN}"})
    except:
        return Response(status.HTTP_404_NOT_FOUND)

    if resp_data.json()['status']:
        try:
            TransferModel.objects.create(
                wallet=wallet, tr_id=resp_data.json()['result']['tr_id'],
                status=False, amount=data['amount'],
                destination=data['number'], type=False
            )
        except:
            return Response({'status': True, 'message': "TransferModel object create failed!",
                             'tr_id': resp_data.json()['result']['tr_id']})
        return Response(resp_data.json())
    else:
        token = login_to()
        try:
            resp_data = requests.post(url=WALLET_URL, json=payload, headers={"token": f"{token}"})
        except:
            return Response({'message': 'Service is not working.'})
        try:
            TransferModel.objects.create(
                wallet=wallet, tr_id=resp_data.json()['result']['tr_id'],
                status=False, amount=data['amount'],
                destination=data['number'], type=True
            )
        except:
            return Response({'status': True, 'message': "TransferModel object create failed!",
                             'tr_id': resp_data.json()['result']['tr_id']})
    return Response(resp_data.json())


def confirm_transfer_service(data):
    payload = {
        "id": "{{$randomUUID}}",
        "method": "transfer.confirm",
        "params": {
            "tr_id": f"{data['tr_id']}",
            "code": f"{data['code']}",
        }
    }

    try:
        resp_data = requests.post(url=WALLET_URL, json=payload, headers={"token": f"{settings.WALLET_TOKEN}"})
    except:
        return Response({"status": False, "message": "Service is not working!"}, status.HTTP_400_BAD_REQUEST)

    resp_data = resp_data.json()
    if resp_data["status"]:
        try:
            transfer = TransferModel.objects.get(tr_id=data['tr_id'])
        except TransferModel.DoesNotExist:
            return Response({'status': True, 'message': "TransferModel object update failed!",
                             'tr_id': data['tr_id']})

        transfer.status = True
        transfer.save()
        return Response(resp_data)
    elif resp_data['error']['code'] == "404":
        token = login_to()
        try:
            resp_data = requests.post(url=WALLET_URL, json=payload, headers={"token": f"{token}"})
        except:
            return Response({'message': 'Service is not working.'})

        resp_data = resp_data.json()

        try:
            transfer = TransferModel.objects.get(tr_id=data['tr_id'])
        except TransferModel.DoesNotExist:
            return Response({'status': True, 'message': "TransferModel object update failed!",
                             'tr_id': data['tr_id']}, resp_data)

        transfer.status = True
        transfer.save()
        print("Success")
        return Response({"status": True}, resp_data)
    else:
        return Response({"status": False}, resp_data)
