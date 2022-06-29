from uuid import uuid4

from django.db import models
from django.conf import settings

from accounts.models import Account
from courses.models.categories import CategoriesModel, SubCategoriesModel


def upload_location(instance, filename):
    ext = filename.split('.')[-1]
    file_path = 'course/covers/{title}'.format(title='{}.{}'.format(uuid4().hex, ext))
    return file_path


class CourseModel(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, verbose_name="tarriff")
    lang = models.CharField(max_length=255)
    level = models.CharField(max_length=255)
    category = models.ForeignKey(CategoriesModel, related_name='courses', on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(SubCategoriesModel, related_name='courses', on_delete=models.SET_NULL, null=True)
    course_owner = models.ForeignKey(Account, related_name='courses', on_delete=models.CASCADE)
    key_words = models.CharField(max_length=255)
    what_to_learn = models.TextField()
    whom_this_course = models.TextField()
    students = models.CharField(max_length=255)
    price = models.BigIntegerField()
    short_descr = models.TextField()
    recommendation = models.TextField()
    exchange_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    discount_price = models.FloatField(default=0, null=True)
    cover_img = models.ImageField(upload_to=upload_location, null=True, blank=True)

    def __str__(self):
        return self.name


class FavCoursesModel(models.Model):
    course = models.ForeignKey(CourseModel, related_name='fav_course', blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, related_name='fav_course', blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(f"{self.user.phone_number} - {self.course.name}")

#
# class ModuleModel(models.Model):
#     course = models.ForeignKey(CourseModel, related_name='module', blank=True, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     description = models.TextField()
