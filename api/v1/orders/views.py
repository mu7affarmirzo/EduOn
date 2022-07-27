import requests
from decouple import config
from django.conf import settings
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.orders.serializers import CartSerializer, CartSummarySerializer
from api.v1.orders.service import get_cart_total_price, get_wallet, proceed_transfer
from courses.models.courses import CourseModel
from orders.models.cart import CartModel
from wallet.models import WalletModel, TransferModel
from api.v1.wallet.utils import login_to

EDUON_WALLET = config('EDUON_WALLET')

WALLET_URL = config('WALLET_URL')
HEADER = {"token": f"{settings.WALLET_TOKEN}"}


class CartListView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return CartModel.objects.get(pk=pk)
        except CartModel.DoesNotExist:
            raise Http404

    @swagger_auto_schema(tags=['cart'])
    def get(self, request, format=None):
        account = request.user
        snippets = CartModel.objects.filter(owner=account)
        resp_serializer = CartSummarySerializer({"items": snippets})
        return Response(resp_serializer.data)

    @swagger_auto_schema(tags=['cart'], request_body=CartSerializer)
    def post(self, request, format=None):
        account = request.user
        cart = CartModel(owner=account)

        serializer = CartSerializer(cart, data=request.data)
        if serializer.is_valid():
            if CartModel.objects.filter(course=request.data['course'], owner=account).exists():
                return Response({'message': 'This course already exists'})
            else:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return CartModel.objects.get(pk=pk)
        except CartModel.DoesNotExist:
            raise Http404

    @swagger_auto_schema(tags=['cart'])
    def delete(self, request, pk, format=None):
        try:
            course = CartModel.objects.get(id=pk)
        except CartModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if course.owner.id != user.id:
            return Response({'response': "You don't have the permission to delete that."})
        course = self.get_object(pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(tags=['payment-proceed'], method="post")
@api_view(["POST"])
def proceed_payment(request):
    account = request.user
    #TODO: call cart
    wallet = get_wallet(account)
    total_price = get_cart_total_price(account)
    status_order = proceed_transfer(wallet, total_price)

    return status_order


class ProceedOrder(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return CartModel.objects.get(pk=pk)
        except CartModel.DoesNotExist:
            raise Http404

    @staticmethod
    def get_wallet(account):
        try:
            return WalletModel.objects.get(owner=account)
        except WalletModel.DoesNotExist:
            raise Http404

    @staticmethod
    def get_cart_items(account):
        try:
            return CartModel.objects.filter(owner=account).values()
        except CartModel.DoesNotExist:
            raise Http404

    def cancel_transfer(self, tr_id):
        payload = {
            "id": "{{$randomUUID}}",
            "method": "transfer.cancel",
            "params": {
                "tr_id": {tr_id}
            }
        }
        resp_data = requests.post(url=WALLET_URL, json=payload, headers={"token": f"{settings.WALLET_TOKEN}"})
        if not resp_data.json()['status']:
            token = login_to()
            try:
                resp_data = requests.post(url=WALLET_URL, json=payload, headers={"token": f"{token}"})
            except:
                return {'message': False}
            return resp_data.json()
        else:
            return resp_data.json()

    def transfer_money(self, wallet, receiver, amount, is_referral):
        if is_referral:
            edu_on_share = amount * 0.1
            speaker_share = amount - edu_on_share
        else:
            edu_on_share = amount * 0.3
            speaker_share = amount - edu_on_share

        payload = {
            "id": "{{$randomUUID}}",
            "method": "transfer.proceed",
            "params": {
                "number": f"{wallet.card_number}",
                "expire": f"{wallet.expire}",
                "receiver": f"{receiver}",
                "amount": f"{speaker_share}",
            }
        }
        eduon_payload = {
            "id": "{{$randomUUID}}",
            "method": "transfer.proceed",
            "params": {
                "number": f"{wallet.card_number}",
                "expire": f"{wallet.expire}",
                "receiver": f"{EDUON_WALLET}",
                "amount": f"{edu_on_share}",
            }
        }

        try:
            speaker_resp_data = requests.post(url=WALLET_URL, json=payload, headers={"token": f"{settings.WALLET_TOKEN}"})
            if speaker_resp_data.json()['status']:
                eduon_resp_data = requests.post(url=WALLET_URL, json=eduon_payload,
                                                headers={"token": f"{settings.WALLET_TOKEN}"})
                if not eduon_resp_data.json()['status']:
                    self.cancel_transfer(speaker_resp_data.json()['result']['tr_id'])
                    context = {
                        'status': True,
                        'tr_id_speaker': speaker_resp_data.json()['result']['tr_id'],
                        'tr_id_eduon': eduon_resp_data.json()['result']['tr_id']
                    }
                    return context
                else:
                    context = {
                        'status': True,
                        'tr_id_speaker': speaker_resp_data.json()['result']['tr_id'],
                        'tr_id_eduon': eduon_resp_data.json()['result']['tr_id']
                    }
                    return context
            else:
                token = login_to()
                try:
                    speaker_resp_data = requests.post(url=WALLET_URL, json=payload,
                                                      headers={"token": f"{token}"})
                    if speaker_resp_data.json()['status']:
                        eduon_resp_data = requests.post(url=WALLET_URL, json=eduon_payload,
                                                        headers={"token": f"{token}"})
                        if not eduon_resp_data.json()['status']:
                            self.cancel_transfer(speaker_resp_data.json()['result']['tr_id'])
                            context = {
                                'status': True,
                                'tr_id_speaker': speaker_resp_data.json()['result']['tr_id'],
                                'tr_id_eduon': eduon_resp_data.json()['result']['tr_id']
                            }
                            return context
                        else:
                            context = {
                                'status': True,
                                'tr_id_speaker': speaker_resp_data.json()['result']['tr_id'],
                                'tr_id_eduon': eduon_resp_data.json()['result']['tr_id']
                            }
                            return context

                except:
                    return {'status': False, 'message': "Transaction failed!"}
                # TODO: remove from cart and add to enrolled course

            try:
                # TODO: change TransferModel to many to many relation
                # for enrolled course
                TransferModel.objects.create(wallet=wallet, tr_id=speaker_resp_data.json()['result']['tr_id'])
                # for speaker
                TransferModel.objects.create(wallet=receiver, tr_id=speaker_resp_data.json()['result']['tr_id'])
            except:
                return {'status': True, 'message': "TransferModel object create failed!", 'tr_id': speaker_resp_data.json()['result']['tr_id']}

            return {'status': True, 'tr_id': speaker_resp_data.json()['result']['tr_id']}
        except:
            return {'status': False, 'message': "Transaction failed!"}

    @swagger_auto_schema(tags=['order'])
    def post(self, request, format=None):
        account = request.user
        wallet = self.get_wallet(account)
        cart = self.get_cart_items(account)

        transfer_info_context = {
            'wallet': wallet.card_number,
            'expire': wallet.expire
        }

        for course in cart:
            # TODO: exception for each course
            try:
                each_course = CourseModel.objects.get(id=course['course_id'])
                # TODO: optimization needed for better exception handling
            except CourseModel.DoesNotExist:
                transfer_info_context[f'{course}'] = {
                    'status': False,
                    'message': 'Retrieving this course failed!'
                }
                return Response(transfer_info_context)

            transfer_info_context[f'{each_course}'] = {
                    'speakers_wallet': str(each_course.course_owner.wallet),
                    'speakers_wallet_expire': str(each_course.course_owner.wallet.expire),
                    'transfer_status': str(self.transfer_money(
                        wallet,
                        each_course.course_owner.wallet,
                        each_course.price,
                        course['is_referral']
                    ))
                }

        return Response(transfer_info_context)







