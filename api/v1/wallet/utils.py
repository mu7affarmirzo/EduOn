import requests
from decouple import config

WALLET_URL = config('WALLET_URL')
WALLET_TOKEN = config('WALLET_TOKEN')


def create_wallet_util(phone_number):
    header = {"token": f"{WALLET_TOKEN}"}
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
