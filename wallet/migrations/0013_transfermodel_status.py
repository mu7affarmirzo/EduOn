# Generated by Django 3.2.13 on 2022-07-20 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0012_transfermodel_sender'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfermodel',
            name='status',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
