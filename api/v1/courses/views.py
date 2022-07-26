import django_filters
from django.db.models import Q
# from django.db.models.utils import list_to_queryset
from django.http import Http404
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.views import APIView


from accounts.models import Account
from api.v1.accounts.serializers import AccountSerializer
from api.v1.courses.filters import CourseFilter
from api.v1.courses.permissions import IsOwnerOrReadOnly
from api.v1.courses.serializers import *
from courses.models.courses import CourseModel, FavCoursesModel, EnrolledCoursesModel, ModuleModel
from courses.models.categories import CategoriesModel, SubCategoriesModel
from courses.models.comments import CommentsModel


@swagger_auto_schema(tags=['comments'], method='post', request_body=CommentsSerializer)
@permission_classes((IsAuthenticated,))
@api_view(['POST'])
def post_comment(request, format=None):
    account = request.user
    comment = CommentsModel(author=account)
    serializer = CommentsSerializer(comment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentsOptionsView(APIView):

    def get_permissions(self):
        method = self.request.method
        if method == 'GET':
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    def get_object(self, pk):
        try:
            return CommentsModel.objects.get(pk=pk)
        except CommentsModel.DoesNotExist:
            raise Http404

    @swagger_auto_schema(tags=['comments'])
    def get(self, request, pk, format=None):

        snippets = CommentsModel.objects.filter(course_id=pk)
        serializer = CommentsSerializer(snippets, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(tags=['comments'], request_body=CommentsSerializer)
    def put(self, request, pk, format=None):
        try:
            comment = CommentsModel.objects.get(id=pk)
        except CommentsModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if comment.author != user:
            return Response({'response': "You don't have the permission to edit that."})

        comment = self.get_object(pk)
        serializer = CommentsSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=['comments'])
    def delete(self, request, pk, format=None):
        try:
            comment = CommentsModel.objects.get(id=pk)
        except CommentsModel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        course_owner = comment.course.course_owner.id
        user = request.user

        if comment.author.id != user.id or course_owner != user.id:
            return Response({'response': "You don't have the permission to delete that."})
        comment = self.get_object(pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubCategoriesListView(ListAPIView):
    queryset = SubCategoriesModel.objects.all()
    serializer_class = SubCategoryCoursesSerializer

    @swagger_auto_schema(tags=['categories'])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SubCategoriesDetailView(RetrieveAPIView):
    swagger_auto_schema(request_body=SubCategoriesSerializer, tags=['SubCategories'])
    queryset = SubCategoriesModel.objects.filter(courses__is_valid="VALID")
    serializer_class = SubCategoryCoursesSerializer

    @swagger_auto_schema(tags=['categories'])
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CategoriesListView(ListAPIView):
    queryset = CategoriesModel.objects.all()
    serializer_class = CategoriesSerializer

    @swagger_auto_schema(tags=['categories'])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CategoriesDetailView(RetrieveAPIView):
    queryset = CategoriesModel.objects.all()
    serializer_class = CategoriesSerializer

    @swagger_auto_schema(tags=['categories'])
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CourseListFilterView(ListAPIView):
    queryset = CourseModel.objects.filter(is_valid="VALID")
    serializer_class = CourseSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = CourseFilter
    ordering_fields = ['price', 'email']
    ordering = ['price']


@swagger_auto_schema(tags=['categories'], method="get")
@api_view(['GET'])
def filter_by_rating(request, pk):
    print(pk)
    filtered_queryset = []
    queryset = CourseModel.objects.all()
    print(type(queryset))
    for i in queryset:
        if i.course_rating >= pk and i.course_rating <= (pk+1):
            print(i.course_rating)
            filtered_queryset.append(i)
    print(filtered_queryset)
    # filtered_queryset = list_to_queryset(filtered_queryset)
    serializer = CourseSerializer(filtered_queryset)
    print(serializer.data)
    return Response(serializer.data)


class CoursesListView(ListCreateAPIView):
    queryset = CourseModel.objects.all()
    serializer_class = CourseSerializer


    def get_permissions(self):
        method = self.request.method
        if method == 'POST':
            return [IsAuthenticated()]
        else:
            return [AllowAny()]

    def get(self, request, *args, **kwargs):
        snippet = CourseModel.objects.filter(is_valid="VALID")
        course_filter = CourseFilter(request.GET, queryset=snippet)
        ordering_fields = ['price', 'course_rating']

        if course_filter.is_valid():
            snippet = course_filter.qs
        serializer = CourseSerializer(snippet, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(tags=['uploaded courses'], request_body=CourseSerializer)
    def post(self, request, *args, **kwargs):
        account = request.user
        if not account.is_speaker:
            return Response({"status": False, "message": "User is not speaker!"}, status=status.HTTP_400_BAD_REQUEST)

        course = CourseModel(course_owner=account)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CoursesDetailView(RetrieveUpdateDestroyAPIView):
    swagger_auto_schema(request_body=CourseSerializer, tags=['Courses'])
    queryset = CourseModel.objects.filter(is_valid="VALID")
    serializer_class = CourseSerializer


    def get_permissions(self):
        method = self.request.method
        if method == 'PATCH' or method == 'DELETE' or method == 'PUT':
            return [IsAuthenticated(), IsOwnerOrReadOnly]
        else:
            return [AllowAny()]


class ModuleListView(APIView):
    queryset = ModuleModel.objects.all()

    @swagger_auto_schema(tags=['course-modules'])
    def get(self, request, pk):
        snippets = ModuleModel.objects.filter(course_id=pk)
        serializer = ModulesListSerializer(snippets, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(tags=['course-modules'], request_body=ModulesSerializer)
    def put(self, request, pk, format=None):
        module = get_object_or_404(ModuleModel, pk=pk)
        serializer = ModulesSerializer(module, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


@swagger_auto_schema(tags=['course-modules'], method='post', request_body=ModulesSerializer)
@permission_classes((IsAuthenticated,))
@api_view(['POST'])
def modules_post_view(request):
    account = request.user
    if not account.is_speaker:
        return Response({"status": False, "message": "User is not speaker!"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ModulesSerializer(data=request.data)
    if serializer.is_valid():
        try:
            course = CourseModel.objects.get(id=serializer.validated_data['course'].id)
        except CourseModel.DoesNotExist:
            raise Http404

        if course.course_owner != account:
            return Response({"status": False, "message": "This user is not the owner of the course."}, status=status.HTTP_404_NOT_FOUND)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LessonsListView(APIView):
    queryset = LessonsModel.objects.all()
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(tags=['course-modules'], request_body=LessonsSerializer)
    def put(self, request, pk, format=None):
        lesson = get_object_or_404(LessonsModel, pk=pk)
        serializer = LessonsSerializer(lesson, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


@swagger_auto_schema(tags=['course-modules'], method='post', request_body=LessonsSerializer)
@permission_classes((IsAuthenticated,))
@api_view(['POST'])
def lesson_post_view(request):
    account = request.user
    if not account.is_speaker:
        return Response({"status": False, "message": "User is not speaker!"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = LessonsSerializer(data=request.data)
    if serializer.is_valid():
        try:
            module = ModuleModel.objects.get(id=serializer.validated_data['module'].id)
        except CourseModel.DoesNotExist:
            raise Http404

        if module.course.course_owner != account:
            return Response({"status": False, "message": "This user is not the owner of the course."}, status=status.HTTP_404_NOT_FOUND)

        # TODO: restrict video update

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EnrolledCoursesView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return CommentsModel.objects.get(pk=pk)
        except CommentsModel.DoesNotExist:
            raise Http404

    @swagger_auto_schema(tags=['enrolled-courses'])
    def get(self, request, format=None):

        snippets = EnrolledCoursesModel.objects.filter(user=request.user)
        serializer = EnrolledCoursesSerializer(snippets, many=True)
        return Response(serializer.data)


@swagger_auto_schema(method='POST', tags=['Fav courses'], request_body=FavCoursesSerializer)
@permission_classes((IsAuthenticated,))
@api_view(['POST'])
def post_fav_course(request):
    user = request.user
    fav_course = FavCoursesModel(user=user)
    try:
        course = FavCoursesModel.objects.filter(user=user.id)
    except:
        course = {}

    if request.method == 'POST':
        if course.filter(course=request.data['course']).exists():
            return Response({"message": "This course is already in the list!"})

        serializer = FavCoursesSerializer(fav_course, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='GET', tags=['Fav courses'])
@permission_classes((IsAuthenticated,))
@api_view(['GET'])
def list_fav_course(request):
    user = request.user
    try:
        fav_course_values = FavCoursesModel.objects.filter(user=user).values()
    except FavCoursesModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        courses = CourseModel.objects.filter(pk__in=[i['course_id'] for i in fav_course_values])
    except CourseModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


@swagger_auto_schema(method='GET', tags=['uploaded courses'])
@permission_classes((IsAuthenticated,))
@api_view(['GET'])
def my_uploaded_course(request):
    user = request.user
    try:
        uploaded_course = CourseModel.objects.filter(course_owner=user)
    except CourseModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CourseSerializer(uploaded_course, many=True)
        return Response(serializer.data)


@swagger_auto_schema(method='DELETE', tags=['Fav courses'])
@permission_classes([IsAuthenticated, IsOwnerOrReadOnly])
@api_view(['DELETE'])
def remove_fav_courses(request, pk):
    user = request.user
    try:
        course = FavCoursesModel.objects.get(user=user.id, course=pk)
    except FavCoursesModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    course.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(method='POST', tags=['search'], request_body=SearchSerializer)
@api_view(['POST', ])
def search_view(request):

    a = request.data['word']
    if request.method == 'POST':
        queryset_news = CourseModel.objects.filter(
            Q(name__icontains=a) |
            Q(short_descr__icontains=a))

        queryset_tenders = Account.objects.filter(
            Q(is_speaker=True) &
            Q(f_name__icontains=a) |
            Q(l_name__icontains=a) |
            Q(speciality__icontains=a))

        serializer_courses = CourseSerializer(queryset_news, many=True)
        serializer_speakers = AccountSerializer(queryset_tenders, many=True)
        new_data = {
            "found_courses": serializer_courses.data,
            "found_speakers": serializer_speakers.data
        }

        return Response(new_data)

