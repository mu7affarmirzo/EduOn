from twilio.rest import Client
from eduon_v1.settings import ACCOUNT_ID, AUTH_TOKEN
client = Client(ACCOUNT_ID, AUTH_TOKEN)


def send_sms(account, active):
    if active:
        message = client.messages.create(
            body=f"Your verification code: {account.codemodel.number}",
            from_='+16204728813',
            to=account.phone_number
        )
