from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from accounts.models.country import DistrictModel
from api.v1.wallet.utils import create_wallet_util
from wallet.models import WalletModel, VoucherModel


def upload_location(instance, filename):
    ext = filename.split('.')[-1]
    file_path = 'accounts/avatars/{user_id}-{phone_number}'.format(
        user_id=str(instance.id), phone_number='{}.{}'.format(uuid4().hex, ext))
    return file_path


class MyAccountManager(BaseUserManager):
    def create_user(self, f_name, phone_number, password=None):

        if not phone_number:
            raise ValueError("Users must have phone number")

        user = self.model(
            f_name=f_name,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, f_name, phone_number, password):
        user = self.create_user(
            f_name=f_name,
            password=password,
            phone_number=phone_number,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_speaker = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=20, unique=True)
    f_name = models.CharField(max_length=50, blank=True, null=True)
    l_name = models.CharField(max_length=50, blank=True, null=True)
    sex = models.CharField(max_length=50, blank=True, null=True)
    date_birth = models.DateTimeField(blank=True, null=True)
    district = models.ForeignKey(DistrictModel, on_delete=models.SET_NULL, null=True, blank=True)
    speciality = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to=upload_location, null=True, blank=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_speaker = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['f_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    class Meta:
        app_label = "accounts"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_wallet(sender, instance=None, created=False, **kwargs):
    if created:

        data = create_wallet_util(instance.phone_number)
        print(f"data_inside_db: {data}")
        card_number = data['result']['card_number']
        expire = data['result']['expire']

        WalletModel.objects.create(
            owner=instance,
            card_number=card_number,
            expire=expire,
        )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_voucher(sender, instance=None, created=False, **kwargs):
    if created:
        value = 50000

        VoucherModel.objects.create(
            owner=instance,
            value=value,
        )
