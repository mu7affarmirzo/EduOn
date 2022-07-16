import random

import requests
from django.http import HttpResponse, Http404
from drf_yasg.utils import swagger_auto_schema
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.authtoken.models import Token
from urllib.error import HTTPError

from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


from accounts.models import Otp, DeviceModel
from accounts.models.account import Account
from api.v1.accounts.serializers import RegistrationSerializer, AccountSerializer, OtpSerializer, \
    AccountPropertiesSerializers, ChangePasswordSerializer, DevicesSerializer, DeactivateAccountSerializer, \
    StepTwoSerializer, BecomeSpeakerSerializers


@swagger_auto_schema(method="post", tags=["accounts"], request_body=OtpSerializer)
@api_view(['POST'])
def step_one(request):
    if request.method == 'POST':

        sms_url = 'https://sms.unired.uz/api/sms'
        auth_token = 'fa373050-809b-44aa-8d87-1c29220cd242'
        hed = {'Authorization': 'Bearer ' + auth_token}

        request_data = request.data
        sms_code = str(random.randint(10000, 99999))

        data = {
            'method': 'send',
            'params': [{
                'phone': request_data['mobile'],
                'content': sms_code
            }],
        }
        try:
            r = requests.post(sms_url, json=data, headers=hed)
        except HTTPError:
            raise Http404

        enc_otp = pbkdf2_sha256.encrypt(sms_code, rounds=12000, salt_size=32)

        serializer_data = {
            'mobile': request_data['mobile'],
            'otp': enc_otp,
            # 'lang': request_data['lang']
        }

        otp_code = Otp()
        serializer = OtpSerializer(otp_code, serializer_data)
        data = {}

        if serializer.is_valid():
            serializer.save()
            data = {
                'success': "Successfully sent and added",
                'otp_generated': enc_otp,
                'sms_service_response': r.json(),
            }
            return Response(data=data)

        return Response(r.json())


@swagger_auto_schema(method="post", tags=["accounts"], request_body=StepTwoSerializer)
@api_view(['POST'])
def step_two(request):
    if request.method == 'POST':
        data = request.data
        context = {}
        try:
            mobile_user = Otp.objects.get(otp=data['otp_token'])
        except:
            return Response({'status': False, 'message': 'This token has not been found'})

        if pbkdf2_sha256.verify(data['otp'], mobile_user.otp):
            try:
                user = Account.objects.get(phone_number=mobile_user.mobile)
            except:
                return Response({'status': True, 'message': 'This user should be registered!'})

            refresh = RefreshToken.for_user(user)
            context['jwt_token'] = {
                'status': True,
                'message': 'This user had been registered before',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(context)
        else:
            return Response({'status': False, 'message': 'The code is not correct'})

    return Response({'status': True, 'message': 'Code verified!'})


@swagger_auto_schema(method="post", tags=["accounts"], request_body=RegistrationSerializer)
@api_view(['POST', ])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "successfully registered a new user."
            data['email'] = account.email
            data['phone_number'] = account.phone_number
            refresh = RefreshToken.for_user(account)
            data['jwt_token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        else:
            data = serializer.errors
        return Response(data)


@swagger_auto_schema(method="get", tags=["accounts"])
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def account_list_view(request):

    if request.method == 'GET':
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)


@swagger_auto_schema(method="get", tags=["accounts"])
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def account_detail_view(request):

    if request.method == 'GET':
        account = Account.objects.get(id=request.user.id)
        serializer = AccountSerializer(account)
        return Response(serializer.data)


@swagger_auto_schema(method="get", tags=["accounts"])
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def speaker_detail_view(request, pk):

    if request.method == 'GET':
        account = Account.objects.get(id=pk)
        serializer = AccountSerializer(account)
        return Response(serializer.data)


@swagger_auto_schema(method="post", tags=["accounts"], request_body=DeactivateAccountSerializer)
@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def deactivate_account_view(request):

    if request.method == 'POST':
        accounts = Account.objects.get(id=request.user.id)
        serializer = DeactivateAccountSerializer(accounts, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = "Account has been deactivated!"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method="put", tags=["accounts"], request_body=AccountPropertiesSerializers)
@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def update_account_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = AccountPropertiesSerializers(account, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = "Account has been updated!"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method="put", tags=["accounts"], request_body=BecomeSpeakerSerializers)
@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def become_speaker_view(request):

    if request.method == 'PUT':
        serializer = BecomeSpeakerSerializers(request.user, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = "Account has been updated!"
            return Response(data=data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(UpdateAPIView):

    queryset = Account.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


@swagger_auto_schema(method="put", tags=["accounts"], request_body=AccountPropertiesSerializers)
@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def update_password_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ChangePasswordSerializer(account, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = "Account password updated successfully"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DevicesListView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return DeviceModel.objects.get(pk=pk)
        except DeviceModel.DoesNotExist:
            raise Http404

    @swagger_auto_schema(tags=['devices'])
    def get(self, request, format=None):
        devices = DeviceModel.objects.filter(owner=request.user)
        serializer = DevicesSerializer(devices, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(tags=['devices'], request_body=DevicesSerializer)
    def post(self, request, format=None):
        print(f"User-Agent: {request.headers['User-Agent']} - Origin: {request.headers['Origin']} - Host: {request.headers['Origin']}")
        account = request.user
        device = DeviceModel(owner=account)
        serializer = DevicesSerializer(device, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DevicesDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return DeviceModel.objects.get(pk=pk)
        except DeviceModel.DoesNotExist:
            raise Http404

    @swagger_auto_schema(tags=['devices'], request_body=DevicesSerializer)
    def put(self, request, pk, format=None):
        try:
            device = DeviceModel.objects.get(id=pk)
        except DeviceModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if device.owner != user:
            return Response({'response': "You don't have the permission to edit that."})

        device = self.get_object(pk)
        serializer = DevicesSerializer(device, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=['devices'])
    def delete(self, request, pk, format=None):
        try:
            device = DeviceModel.objects.get(id=pk)
        except DeviceModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if device.owner.id != user.id:
            return Response({'response': "You don't have the permission to delete that."})
        device = self.get_object(pk)
        device.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
