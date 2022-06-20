import requests
from decouple import config
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.orders.serializers import CartSerializer, CartSummarySerializer
from courses.models.courses import CourseModel
from orders.models.cart import CartModel
from wallet.models import WalletModel, TransferModel
from api.v1.wallet.utils import login_to
from eduon_v1.settings import WALLET_TOKEN

WALLET_URL = config('WALLET_URL')
HEADER = {"token": f"{WALLET_TOKEN}"}

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


class ProceedOrder(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return CartModel.objects.get(pk=pk)
        except CartModel.DoesNotExist:
            raise Http404

    def get_wallet(self, account):
        try:
            return WalletModel.objects.get(owner=account)
        except WalletModel.DoesNotExist:
            raise Http404

    def get_cart_items(self, account):
        try:
            return CartModel.objects.filter(owner=account).values()
        except CartModel.DoesNotExist:
            raise Http404

    @staticmethod
    def transfer_money(wallet, receiver, amount):
        payload = {
            "id": "{{$randomUUID}}",
            "method": "transfer.proceed",
            "params": {
                "number": f"{wallet.card_number}",
                "expire": f"{wallet.expire}",
                "receiver": f"{receiver}",
                "amount": f"{amount}",
            }
        }
        try:
            resp_data = requests.post(url=WALLET_URL, json=payload, headers=HEADER)
            if resp_data.json()['status']:
                return True
            else:
                token = login_to()
                try:
                    resp_data = requests.post(url=WALLET_URL, json=payload, headers={"token": f"{token}"})
                    # for enrolled course
                    TransferModel.objects.create(wallet=wallet, tr_id=resp_data.json()['result']['tr_id'])
                    # for speaker
                    TransferModel.objects.create(wallet=receiver, tr_id=resp_data.json()['result']['tr_id'])
                except:
                    return "Failed latest"
            return {'status': True, 'tr_id': resp_data.json()['result']['tr_id']}
        except:
            return "Failed"

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
                transfer_info_context[f'{each_course}'] = {
                        'speakers_wallet': str(each_course.course_owner.wallet),
                        'speakers_wallet_expire': str(each_course.course_owner.wallet.expire),
                        'transfer_status': str(self.transfer_money(
                            wallet,
                            each_course.course_owner.wallet,
                            each_course.price
                        ))
                    }

            except CourseModel.DoesNotExist:
                pass

        return Response(transfer_info_context)







