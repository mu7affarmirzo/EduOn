import requests
from decouple import config
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.wallet.serializers import TransferSerializer
from wallet.models import WalletModel, TransferModel

WALLET_URL = config('WALLET_URL')
WALLET_TOKEN = config('WALLET_TOKEN')
HEADER = {"token": f"{WALLET_TOKEN}"}

PAYLOAD = {
    "id": "{{$randomUUID}}",
    "method": "",
    "params": {}
}

@swagger_auto_schema(method="get", tags=["wallet"])
@permission_classes((IsAuthenticated,))
@api_view(['GET'])
def info_wallet(request):
    try:
        wallet = WalletModel.objects.get(owner=request.user)
    except WalletModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    payload = {
        "id": "{{$randomUUID}}",
        "method": "wallet.info",
        "params": {
            "number": wallet.card_number,
            "expire": wallet.expire
            }
        }
    data = requests.post(url=WALLET_URL, json=payload, headers=HEADER)

    return Response(data.json())


@swagger_auto_schema(method="post", tags=["wallet"], request_body=TransferSerializer)
@permission_classes((IsAuthenticated,))
@api_view(['POST'])
def transfer_to_wallet(request):
    try:
        wallet = WalletModel.objects.get(owner=request.user)
    except WalletModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializers = TransferSerializer(data=request.data)
        if serializers.is_valid():
            data = serializers.data
            print(data['number'])
            print(wallet.card_number)

            payload = {
                "id": "{{$randomUUID}}",
                "method": "transfer.proceed",
                "params": {
                    "number": f"{data['number']}",
                    "expire": f"{data['expire']}",
                    "receiver": f"{wallet.card_number}",
                    "amount": f"{data['amount']}",
                }
            }
            try:
                resp_data = requests.post(url=WALLET_URL, json=payload, headers=HEADER)
                TransferModel.objects.create(wallet=wallet, tr_id=resp_data.json()['result']['tr_id'])
            except:
                return Response(status.HTTP_404_NOT_FOUND)

            return Response(resp_data.json())
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)






# @swagger_auto_schema(method="get", tags=["wallet"])
# @api_view(['GET'])
# def create_wallet(request):
#     header = {"token": f"{WALLET_TOKEN}"}
#     payload = {
#         "id": "{{$randomUUID}}",
#         "method": "wallet.create",
#         "params": {
#             "name": "Test card",
#             "phone": "998998465592",
#             "wallet_name": "Test card"
#         }
#     }
#
#     data = requests.post(url=WALLET_URL, json=payload, headers=header)
#
#     return Response(data.json())


