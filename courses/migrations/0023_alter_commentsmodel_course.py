# Generated by Django 3.2.13 on 2022-07-19 06:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0022_alter_enrolledcoursesmodel_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentsmodel',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='courses.coursemodel'),
        ),
    ]
