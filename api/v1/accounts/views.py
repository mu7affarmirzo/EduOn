from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token

from accounts.models.account import Account
from api.v1.accounts.serializers import RegistrationSerializer, AccountSerializer, CompleteRegistrationSerializer

from api.v1.accounts.utils import send_sms


@swagger_auto_schema(method="post", tags=["Account"], request_body=RegistrationSerializer)
@api_view(['POST', ])
def registration_view(request):

    """
    Step 1. Take phone number or email to check database whether this user exists
    Step 2. SMS Verification
    Step 3. Complete Registration and save user to the database

    """

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()

            # sending sms
            send_sms(account, False)

            token = Token.objects.get(user=account).key
            data = {
                'response': "successfully registered a new user.",
                'email': account.email,
                'phone_number': account.phone_number,
                'otp_code': account.codemodel.number,
                'token': token,
            }
        else:
            data = serializer.errors
        return Response(data)


@swagger_auto_schema(method="post", tags=["Account"])
@api_view(['POST', ])
def sms_verification_view(request):

    if request.method == 'POST':
        user = Account.objects.get(auth_token=request.data['token'])
        sms_code_from_user = request.data['sms']

        data = {
            'user': user.email,
            'sms_code': user.codemodel.number,
            'sms_code_from_user': sms_code_from_user
        }
        if str(sms_code_from_user) == str(user.codemodel.number):
            data['response'] = "Success!"
            user.is_active = True
            user.save()
            data['user_status'] = user.is_active
            return Response(data)
        else:
            data['response'] = "Wrong code"
            return Response(data)


@swagger_auto_schema(method="post", tags=["Account"], request_body=CompleteRegistrationSerializer)
@api_view(['POST', ])
def complete_registration_view(request):
    # try:
    #     account = request.user
    # except Account.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        account = Account.objects.get(auth_token=request.data['token'])
        data = request.data
        data.pop('token')
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = CompleteRegistrationSerializer(account, data=data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = "Registration completed!"
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method="get", tags=["Account"])
@api_view(['GET', ])
def account_list_view(request):

    if request.method == 'GET':
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)


def hi(request):
    return HttpResponse('Hello')
