from rest_framework import serializers
from accounts.models.account import Account
from twilio.rest import Client
from eduon_v1.settings import ACCOUNT_ID, AUTH_TOKEN


client = Client(ACCOUNT_ID, AUTH_TOKEN)


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['email', 'phone_number', 'password', 'password2']

    def save(self, **kwargs):

        if self.validated_data['email'] is not None:
            account = Account(
                email=self.validated_data['email'],
                is_active=False
            )
        elif self.validated_data['phone_number'] is not None:
            account = Account(
                phone_number=self.validated_data['phone_number'],
                is_active=False
            )
        else:
            raise Exception("Email or Phone number must have")

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Password must match!'})
        account.set_password(password)
        account.save()
        return account


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = "__all__"


class CompleteRegistrationSerializer(serializers.ModelSerializer):
    # token = serializers.CharField(max_length=50, null=True, blank=True)

    class Meta:
        model = Account
        fields = ['f_name', 'l_name', 'sex', 'date_birth', 'district', 'speciality']
