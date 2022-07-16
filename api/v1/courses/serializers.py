from rest_framework import serializers

from courses.models.categories import CategoriesModel, SubCategoriesModel
from courses.models.courses import CourseModel, FavCoursesModel, EnrolledCoursesModel
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


class SubCategoriesSerializer(serializers.ModelSerializer):
    # courses = CourseSerializer(many=True)

    class Meta:
        model = SubCategoriesModel
        fields = "__all__"


class CategoriesSerializer(serializers.ModelSerializer):
    subcategory = SubCategoriesSerializer(many=True)

    class Meta:
        model = CategoriesModel
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):

    course_owner = serializers.SerializerMethodField('get_username_from_author')
    enrolled_students = serializers.SerializerMethodField(read_only=True)
    course_rating = serializers.SerializerMethodField(read_only=True)

    def get_enrolled_students(self, obj):
        return obj.enrolled_course.count()

    def get_course_rating(self, obj):
        overall_rating = 0

        for i in obj.rating.values():
            overall_rating += i['rating']

        if not obj.rating.count() == 0:
            overall_rating = overall_rating/obj.rating.count()

        return {'rating': "{:.1f}".format(overall_rating), 'voters_number': obj.rating.count()}

    class Meta:
        model = CourseModel
        fields = '__all__'

    def get_username_from_author(self, obj):
        try:
            username = f"{obj.course_owner.f_name} {obj.course_owner.l_name}"
        except:
            username = obj.course_owner.phone_number
        return username


class FavCoursesSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavCoursesModel
        fields = [
            'course',
        ]


class EnrolledCoursesSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = EnrolledCoursesModel
        fields = [
            'course',
        ]


class SubCategoryCoursesSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True)

    class Meta:
        model = SubCategoriesModel
        fields = [
            'courses',
        ]



