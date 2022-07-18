import os
import requests

from decouple import config
from django.db.utils import IntegrityError
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.wallet.serializers import *
from api.v1.wallet.utils import login_to, withdraw_from_wallet_service, transfer_service
from django.conf import settings
from wallet.models import WalletModel, TransferModel, CardModel, VoucherModel



EDUON_WALLET = config('EDUON_WALLET')
WALLET_URL = config('WALLET_URL')
HEADER = {"token": f"{settings.WALLET_TOKEN}"}


@permission_classes((IsAuthenticated, ))
@swagger_auto_schema(method="get", tags=["wallet"])
@api_view(['GET'])
def transactions_history_view(request):
    account = request.user
    transactions = TransferModel.objects.filter(wallet=account.wallet)
    serializer = TransactionSerializer(transactions, many=True)

    return Response(serializer.data)


@permission_classes((IsAuthenticated, ))
@swagger_auto_schema(method="get", tags=["wallet"])
@api_view(['GET'])
def info_wallet(request):


    if str(request.user) == "AnonymousUser":
        return Response(status=status.HTTP_403_FORBIDDEN)
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
    try:
        data = requests.post(url=WALLET_URL, json=payload, headers={"token": f"{settings.WALLET_TOKEN}"})
    except:
        return Response({'message': 'Service is not working.'})

    if data.json()['status']:
        return Response(data.json())
    else:
        token = login_to()
        try:
            data = requests.post(url=WALLET_URL, json=payload, headers={"token": f"{token}"})
        except:
            return Response({'message': 'Service is not working.'})
        return Response(data.json())


PAYLOAD = {
    "id": "{{$randomUUID}}",
    "method": "",
    "params": {}
}


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
            return transfer_service(wallet, data)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method="post", tags=["wallet"], request_body=TransferSerializer)
@permission_classes((IsAuthenticated,))
@api_view(['POST'])
def withdraw_from_wallet(request):
    try:
        wallet = WalletModel.objects.get(owner=request.user)
    except WalletModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializers = TransferSerializer(data=request.data)
        if serializers.is_valid():
            data = serializers.data

            resp_data = withdraw_from_wallet_service(wallet, data)
            return resp_data
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method="post", tags=["wallet"], request_body=WalletHistorySerializer)
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def history_wallet(request):
    try:
        wallet = WalletModel.objects.get(owner=request.user)
    except WalletModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializers = WalletHistorySerializer(data=request.data)
        if serializers.is_valid():
            data = serializers.data

            payload = {
                "id": "{{$randomUUID}}",
                "method": "wallet.history",
                "params": {
                    "number": wallet.card_number,
                    "expire": wallet.expire,
                    "start_date": f"{data['start_date']}",
                    "end_date": f"{data['end_date']}",
                    }
                }
            try:
                data = requests.post(url=WALLET_URL, json=payload, headers={"token": f"{settings.WALLET_TOKEN}"})
            except:
                return Response(status.HTTP_404_NOT_FOUND)

            if data.json()['status']:
                return Response(data.json())
            else:
                token = login_to()
                try:
                    data = requests.post(url=WALLET_URL, json=payload, headers={"token": f"{token}"})
                except:
                    return Response({'message': 'Service is not working.'})

            return Response(data.json())
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class CardListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['card'])
    def get(self, request, format=None):
        account = request.user
        card = CardModel.objects.filter(owner=account)
        serializer = CardSerializer(card, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(tags=['card'], request_body=CardAddSerializer)
    def post(self, request, format=None):
        account = request.user
        card = CardModel(owner=account)
        serializer = CardAddSerializer(card, data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
            except IntegrityError:
                return Response({"status": False, "message": "This card already added!"})
            resp_serializer = CardSerializer(card)
            return Response(resp_serializer.data, status=status.HTTP_201_CREATED)
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

    @swagger_auto_schema(tags=['card'], request_body=CardSerializer)
    def put(self, request, pk, format=None):
        card = self.get_object(pk)

        if card.owner.id != request.user.id:
            return Response({'response': "You don't have the permission to get that."})

        serializer = CardSerializer(card, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=['card'])
    def delete(self, request, pk, format=None):
        card = self.get_object(pk)
        user = request.user

        if card.owner.id != user.id:
            return Response({'response': "You don't have the permission to delete that."})
        card.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VoucherListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=['wallet'])
    def get(self, request, format=None):
        account = request.user
        vouchers = VoucherModel.objects.filter(owner=account)
        serializer = VoucherSerializer(vouchers, many=True)
        return Response(serializer.data)
