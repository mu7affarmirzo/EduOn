# Generated by Django 3.2.13 on 2022-07-29 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0026_alter_lessonsmodel_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonsmodel',
            name='duration',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
