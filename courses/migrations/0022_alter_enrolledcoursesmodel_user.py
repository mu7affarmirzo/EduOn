# Generated by Django 3.2.13 on 2022-07-19 05:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0021_alter_coursemodel_is_valid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrolledcoursesmodel',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='enrolled_student', to=settings.AUTH_USER_MODEL),
        ),
    ]
