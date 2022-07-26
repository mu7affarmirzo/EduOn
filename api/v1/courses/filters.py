import django_filters as filters
from django.db.models import F, Case, When, BooleanField

from courses.models.courses import CourseModel


class CourseFilter(filters.FilterSet):
    rating = filters.OrderingFilter(method='filter_rating')

    class Meta:
        model = CourseModel
        fields = ['category', 'subcategory']

