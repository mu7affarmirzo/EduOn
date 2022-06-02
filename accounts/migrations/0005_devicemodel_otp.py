# Generated by Django 3.2.13 on 2022-06-02 05:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_account_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Otp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(blank=True, max_length=50, null=True)),
                ('otp', models.CharField(blank=True, max_length=300, null=True)),
                ('additional', models.CharField(blank=True, max_length=50, null=True)),
                ('lang', models.CharField(blank=True, max_length=50, null=True)),
                ('is_expired', models.SmallIntegerField(blank=True, default=False, null=True)),
                ('tried', models.CharField(blank=True, default=0, max_length=50, null=True)),
                ('is_forgot', models.SmallIntegerField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_name', models.CharField(blank=True, max_length=255, null=True)),
                ('ip', models.CharField(blank=True, max_length=255, null=True)),
                ('imei', models.CharField(blank=True, max_length=255, null=True)),
                ('mac', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('lat', models.CharField(blank=True, max_length=255, null=True)),
                ('long', models.CharField(blank=True, max_length=255, null=True)),
                ('firebase_reg_id', models.CharField(blank=True, max_length=255, null=True)),
                ('uuid', models.CharField(blank=True, max_length=255, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_devices', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
