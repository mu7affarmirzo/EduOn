from rest_framework import serializers

from courses.models.categories import CategoriesModel, SubCategoriesModel
from courses.models.courses import CourseModel, FavCoursesModel
from courses.models.comments import CommentsModel


class CommentsSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username_from_author')

    class Meta:
        model = CommentsModel
        fields = [
            'id',
            'text',
            'date_created',
            'username',
            'course'
        ]

    def get_username_from_author(self, comment):
        username = comment.author.phone_number
        return username


class FavCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavCoursesModel
        fields = [
            'course',
        ]


class SubCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategoriesModel
        fields = "__all__"


class CategoriesSerializer(serializers.ModelSerializer):
    subcategory = SubCategoriesSerializer(many=True)

    class Meta:
        model = CategoriesModel
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModel
        fields = "__all__"


