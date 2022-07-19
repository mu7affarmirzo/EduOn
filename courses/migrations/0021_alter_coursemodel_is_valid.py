# Generated by Django 3.2.13 on 2022-07-18 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0020_alter_coursemodel_is_valid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursemodel',
            name='is_valid',
            field=models.CharField(choices=[('ON HOLD', 'ON HOLD'), ('NOT VALID', 'NOT VALID'), ('VALID', 'VALID')], max_length=25, null=True),
        ),
    ]