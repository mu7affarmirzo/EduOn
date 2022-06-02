from django.db import models
from django.conf import settings

from accounts.models import Account
from courses.models.categories import CategoriesModel, SubCategoriesModel


class CourseModel(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, verbose_name="tarriff")
    lang = models.CharField(max_length=255)
    level = models.CharField(max_length=255)
    category = models.ForeignKey(CategoriesModel, related_name='courses', on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(SubCategoriesModel, related_name='courses', on_delete=models.SET_NULL, null=True)
    course_owner = models.ForeignKey(Account, related_name='courses', on_delete=models.CASCADE)
    image = models.CharField(max_length=255)
    key_words = models.CharField(max_length=255)
    what_to_learn = models.TextField()
    whom_this_course = models.TextField()
    students = models.CharField(max_length=255)
    price = models.BigIntegerField()
    certificates = models.CharField(max_length=255)
    short_descr = models.TextField()
    recommendation = models.TextField()
    exchange_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    discount_price = models.FloatField(default=0, null=True)

    # fav_courses = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='fav_cource', blank=True)

    def __str__(self):
        return self.name


class FavCoursesModel(models.Model):
    course = models.ForeignKey(CourseModel, related_name='fav_course', blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, related_name='fav_course', blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(f"{self.user.phone_number} - {self.course.name}")


