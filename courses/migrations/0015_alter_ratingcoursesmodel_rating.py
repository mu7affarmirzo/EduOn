# Generated by Django 3.2.13 on 2022-06-30 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0014_auto_20220630_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratingcoursesmodel',
            name='rating',
            field=models.CharField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], max_length=255, null=True),
        ),
    ]
