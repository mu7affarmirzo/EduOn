# Generated by Django 3.2.13 on 2022-06-27 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_remove_coursemodel_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursemodel',
            name='certificates',
        ),
    ]
