from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token

from accounts.models.account import Account
from api.v1.accounts.serializers import RegistrationSerializer, AccountSerializer

# swagger_auto_schema

# class AccountView(GenericAPIView):
#     serializer_class = RegistrationSerializer
#
#     def post(self, request):


@swagger_auto_schema(method="post", tags=["Account"], request_body=RegistrationSerializer)
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
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


@swagger_auto_schema(method="get", tags=["Account"])
@api_view(['GET', ])
def account_list_view(request):

    if request.method == 'GET':
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)


def hi(request):
    return HttpResponse('Hello')
