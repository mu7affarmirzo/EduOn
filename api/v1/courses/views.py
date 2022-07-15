from django.http import Http404
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.courses.permissions import IsOwnerOrReadOnly
from api.v1.courses.serializers import SubCategoriesSerializer, CategoriesSerializer, CourseSerializer, \
    FavCoursesSerializer, CommentsSerializer, SubCategoryCoursesSerializer, EnrolledCoursesSerializer
from courses.models.courses import CourseModel, FavCoursesModel, EnrolledCoursesModel
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
    permission_classes = [IsAuthenticated]

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

        if comment.author.id != user.id and course_owner != user.id:
            return Response({'response': "You don't have the permission to delete that."})
        comment = self.get_object(pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




# class CommentsDetailView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get_object(self, pk):
#         try:
#             return CommentsModel.objects.get(pk=pk)
#         except CommentsModel.DoesNotExist:
#             raise Http404
#
#     @swagger_auto_schema(tags=['comments'], request_body=CommentsSerializer)
#     def put(self, request, pk, format=None):
#         try:
#             comment = CommentsModel.objects.get(id=pk)
#         except CommentsModel.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#         user = request.user
#         if comment.author != user:
#             return Response({'response': "You don't have the permission to edit that."})
#
#         comment = self.get_object(pk)
#         serializer = CommentsSerializer(comment, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
#     @swagger_auto_schema(tags=['comments'])
#     def delete(self, request, pk, format=None):
#         try:
#             comment = CommentsModel.objects.get(id=pk)
#         except CommentsModel.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#         course_owner = comment.course.course_owner.id
#         user = request.user
#
#         if comment.author.id != user.id and course_owner != user.id:
#             return Response({'response': "You don't have the permission to delete that."})
#         comment = self.get_object(pk)
#         comment.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class SubCategoriesListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    swagger_auto_schema(request_body=SubCategoriesSerializer, tags=['SubCategories'])
    queryset = SubCategoriesModel.objects.all()
    serializer_class = SubCategoryCoursesSerializer

    # def get(self, request, *args, **kwargs):
    #     return Response({'message': "no photo no video"})


class SubCategoriesDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    swagger_auto_schema(request_body=SubCategoriesSerializer, tags=['SubCategories'])
    queryset = SubCategoriesModel.objects.all()
    serializer_class = SubCategoryCoursesSerializer


class CategoriesListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    swagger_auto_schema(request_body=CategoriesSerializer, tags=['Categories'])
    queryset = CategoriesModel.objects.all()
    serializer_class = CategoriesSerializer


class CategoriesDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    swagger_auto_schema(request_body=CategoriesSerializer, tags=['Categories'])
    queryset = CategoriesModel.objects.all()
    serializer_class = CategoriesSerializer


class CoursesListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    swagger_auto_schema(request_body=CourseSerializer, tags=['Courses'])
    queryset = CourseModel.objects.all()
    serializer_class = CourseSerializer

    @swagger_auto_schema(tags=['uploaded courses'], request_body=CourseSerializer)
    def post(self, request, *args, **kwargs):
        account = request.user
        if not account.is_speaker:
            return Response({"status": False, "message": "User is not speaker!"})

        course = CourseModel(course_owner=account)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CoursesDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
    swagger_auto_schema(request_body=CourseSerializer, tags=['Courses'])
    queryset = CourseModel.objects.all()
    serializer_class = CourseSerializer


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
        fav_course = FavCoursesModel.objects.filter(user=user)
    except FavCoursesModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FavCoursesSerializer(fav_course, many=True)
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


@swagger_auto_schema(method='POST', tags=['Fav courses'])
@permission_classes([IsOwnerOrReadOnly, IsAuthenticated])
@api_view(['POST'])
def add_to_fav_courses(request, pk):
    pass
