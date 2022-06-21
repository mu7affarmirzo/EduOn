from rest_framework import serializers

from courses.models.categories import CategoriesModel, SubCategoriesModel
from courses.models.courses import CourseModel, FavCoursesModel
from courses.models.comments import CommentsModel


class CommentsSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username_from_author')

    class Meta:
        model = CommentsModel
        fields = [
            'text',
            'date_created',
            'course',
            'username'
        ]

    def get_username_from_author(self, instance, comment):
        username = comment.author.phone_number
        return username


class FavCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavCoursesModel
        fields = [
            'course',
        ]


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriesModel
        fields = "__all__"


class SubCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategoriesModel
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModel
        fields = "__all__"


