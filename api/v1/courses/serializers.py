from rest_framework import serializers

from courses.models.categories import CategoriesModel, SubCategoriesModel
from courses.models.courses import CourseModel, FavCoursesModel, EnrolledCoursesModel, ModuleModel, LessonsModel
from courses.models.comments import CommentsModel


class CommentsSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_username_from_author')
    phone = serializers.SerializerMethodField('get_phone_from_author')

    class Meta:
        model = CommentsModel
        fields = [
            'id',
            'text',
            'date_created',
            'user',
            'phone',
            'course'
        ]

    def get_phone_from_author(self, comment):
        phone_number = comment.author.phone_number
        return phone_number

    def get_username_from_author(self, comment):
        try:
            username = f"{comment.author.f_name} {comment.author.l_name}"
        except:
            username = ""
        try:
            profile_picture = comment.author.profile_picture.url
        except:
            profile_picture = ""

        return {"full_name": username, "picture": str(profile_picture)}


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
    course_owner = serializers.SerializerMethodField('get_username_from_author')
    enrolled_students = serializers.SerializerMethodField(read_only=True)
    is_free = serializers.SerializerMethodField(read_only=True)
    course_rating = serializers.SerializerMethodField(read_only=True)
    # course_duration = serializers.SerializerMethodField('get_course_duration')


    def get_is_free(self, obj):
        return True if obj.price == 0 else False

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
        read_only_fields = ('is_valid',)

    def get_username_from_author(self, obj):
        try:
            username = {
                "id": obj.course_owner.id,
                "full_name": f"{obj.course_owner.f_name} {obj.course_owner.l_name}"
            }
        except:
            username = obj.course_owner.id
        return username

    # def get_course_duration(self, obj):
    #     return obj.course_duration


class LessonsPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = LessonsModel
        fields = '__all__'


class LessonsSerializer(serializers.ModelSerializer):

    class Meta:
        model = LessonsModel
        fields = ['module', 'name']


class LessonsIfEnrolledSerializer(serializers.ModelSerializer):

    class Meta:
        model = LessonsModel
        fields = '__all__'


class ModulesListSerializer(serializers.ModelSerializer):
    lessons = LessonsSerializer(many=True)
    module_duration = serializers.SerializerMethodField('get_duration')

    class Meta:
        model = ModuleModel
        fields = '__all__'

    # def get_duration(self, obj):
    #     return obj.module_duration


class WatchModulesSerializer(serializers.ModelSerializer):
    lessons = LessonsIfEnrolledSerializer(many=True)
    module_duration = serializers.SerializerMethodField('get_duration')

    class Meta:
        model = ModuleModel
        fields = '__all__'

    # def get_duration(self, obj):
    #     return obj.module_duration


class ModulesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModuleModel
        fields = '__all__'


class FavCoursesSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavCoursesModel
        fields = [
            'course',
        ]


class FavCoursesListSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

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
    courses = serializers.SerializerMethodField()

    def get_courses(self, subcategory):
        qs = CourseModel.objects.filter(is_valid="VALID", subcategory=subcategory)
        serializer = CourseSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = SubCategoriesModel
        fields = [
            'id',
            'name',
            'courses',
        ]


class SearchSerializer(serializers.Serializer):
    word = serializers.CharField(max_length=255)

    class Meta:
        fields = "__all__"

