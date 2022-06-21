import os

import requests
from decouple import config

# from eduon_v1 import settings
from django.conf import settings
from rest_framework.response import Response

WALLET_URL = config('WALLET_URL')

LOGIN_USERNAME = config('LOGIN_USERNAME')
LOGIN_PASSWORD = config('LOGIN_PASSWORD')


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

