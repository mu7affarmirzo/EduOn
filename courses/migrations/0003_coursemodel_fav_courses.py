# Generated by Django 3.2.13 on 2022-05-24 14:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0002_coursemodel_course_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursemodel',
            name='fav_courses',
            field=models.ManyToManyField(blank=True, related_name='fav_cource', to=settings.AUTH_USER_MODEL),
        ),
    ]
