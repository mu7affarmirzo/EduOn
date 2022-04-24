from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from accounts.models.country import DistrictModel


class MyAccountManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None):
        if not email:
            raise ValueError("Users must have email")
        if not phone_number:
            raise ValueError("Users must have phone number")

        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            phone_number=phone_number,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    f_name = models.CharField(max_length=50, blank=True, null=True)
    l_name = models.CharField(max_length=50, blank=True, null=True)
    sex = models.CharField(max_length=50, blank=True, null=True)
    date_birth = models.DateTimeField(blank=True, null=True)
    district = models.ForeignKey(DistrictModel, on_delete=models.SET_NULL, null=True, blank=True)
    speciality = models.CharField(max_length=255, blank=True, null=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    objects = MyAccountManager()

    def __str__(self):
        return str(self.email)

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
