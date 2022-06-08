import requests
from decouple import config
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.wallet.serializers import TransferSerializer, CardSerializer
from wallet.models import WalletModel, TransferModel, CardModel

WALLET_URL = config('WALLET_URL')
WALLET_TOKEN = config('WALLET_TOKEN')
HEADER = {"token": f"{WALLET_TOKEN}"}

PAYLOAD = {
    "id": "{{$randomUUID}}",
    "method": "",
    "params": {}
}

#
# class IsOwnerOrReadOnly(permissions.BasePermission):
#
#     def has_object_permission(self, request, view, obj):
#
#         if request.method in permissions.SAFE_METHODS:
#             return True
#
#         return obj.owner == request.user


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


class CardListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['card'])
    def get(self, request, format=None):
        account = request.user
        card = CardModel.objects.filter(owner=account)
        serializer = CardSerializer(card, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(tags=['card'], request_body=CardSerializer)
    def post(self, request, format=None):
        account = request.user
        card = CardModel(owner=account)
        serializer = CardSerializer(card, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CardDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return CardModel.objects.get(pk=pk)
        except CardModel.DoesNotExist:
            raise Http404

    @swagger_auto_schema(tags=['card'])
    def get(self, request, pk, format=None):
        card = self.get_object(pk)

        if card.owner.id != request.user.id:
            return Response({'response': "You don't have the permission to get that."})

        serializer = CardSerializer(card)
        return Response(serializer.data)

    @swagger_auto_schema(tags=['card'])
    def delete(self, request, pk, format=None):
        try:
            card = CardModel.objects.get(id=pk)
        except CardModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if card.owner.id != user.id:
            return Response({'response': "You don't have the permission to delete that."})
        card = self.get_object(pk)
        card.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

