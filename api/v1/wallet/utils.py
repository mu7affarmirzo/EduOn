import os
import re

import requests
from decouple import config

from eduon_v1 import settings

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
    try:
        data = requests.post(url=WALLET_URL, json=payload)
        settings.WALLET_TOKEN = data.json()['result']['access_token']
    except:
        return {"status": False}

    return data.json()['result']['access_token']


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
        data = requests.post(url=WALLET_URL, json=payload, headers=header)
    except:
        return {"status": False}

    return data.json()
