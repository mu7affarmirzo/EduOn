from uuid import uuid4

from django.db import models
from django.conf import settings

from accounts.models import Account
from courses.models.categories import CategoriesModel, SubCategoriesModel


RATING_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)

VALIDITY_CHOICES = (
    ('ON HOLD', "ON HOLD"),
    ('NOT VALID', 'NOT VALID'),
    ('VALID', 'VALID'),
)


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
    price = models.BigIntegerField()
    short_descr = models.TextField()
    recommendation = models.TextField()
    exchange_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    discount_price = models.FloatField(default=0, null=True)
    cover_img = models.ImageField(upload_to=upload_location, null=True, blank=True)
    trailer_url = models.URLField(max_length=255, null=True)

    is_valid = models.CharField(max_length=25, choices=VALIDITY_CHOICES, null=True)

    @property
    def is_free(self):
        return True if self.price == 0 else False

    def __str__(self):
        return self.name


class ModuleModel(models.Model):
    course = models.ForeignKey(CourseModel, related_name='module', blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(f"{self.course.name} - {self.name}")


class LessonsModel(models.Model):
    module = models.ForeignKey(ModuleModel, related_name='lessons', blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    video_lesson_url = models.URLField(max_length=255, null=True)
    subtitle_url = models.URLField(max_length=255, null=True)
    about = models.TextField(null=True)
    resource_file = models.FileField(null=True)# TODO:
    duration = models.DurationField(null=True)

    def __str__(self):
        return str(f"{self.module.name} - {self.name}")


class FavCoursesModel(models.Model):
    course = models.ForeignKey(CourseModel, related_name='fav_course', blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, related_name='fav_course', blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(f"{self.user.phone_number} - {self.course.name}")

    class Meta:
        unique_together = ('course', 'user')


class EnrolledCoursesModel(models.Model):
    course = models.ForeignKey(CourseModel, related_name='enrolled_course', blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, related_name='enrolled_course', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(f"{self.user.phone_number} - {self.course.name}")

    class Meta:
        unique_together = ('course', 'user')


class RatingCoursesModel(models.Model):

    course = models.ForeignKey(CourseModel, related_name='rating', blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, related_name='rating', blank=True, null=True, on_delete=models.SET_NULL)
    rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)

    def __str__(self):
        return str(f"{self.user.phone_number} - {self.course.name} - {self.rating}")

    class Meta:
        unique_together = ('course', 'user')
