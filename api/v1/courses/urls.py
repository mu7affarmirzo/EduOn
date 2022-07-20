from django.urls import path, include
from api.v1.courses.views import *

app_name = 'courses'

urlpatterns = [
    path('', CoursesListView.as_view(), name='courses'),
    path('<int:pk>', CoursesDetailView.as_view(), name='courses-detail'),

    path('module/<int:pk>', ModuleListView.as_view(), name='courses-modules-detail'),
    path('module/', modules_post_view, name='courses-modules'),

    path('lesson/<int:pk>', LessonsListView.as_view(), name='courses-lesson-detail'),
    path('lesson/', lesson_post_view, name='courses-lesson'),


    path('subcategories/', SubCategoriesListView.as_view(), name='sub-categories'),
    path('subcategories/<int:pk>', SubCategoriesDetailView.as_view(), name='sub-categories-detail'),
    path('categories/', CategoriesListView.as_view(), name='categories'),
    path('categories/<int:pk>', CategoriesDetailView.as_view(), name='categories-detail'),

    path('comments/', post_comment, name='comments'),
    path('comments/<int:pk>', CommentsOptionsView.as_view(), name='course-comments'),

    path('fav-courses/', post_fav_course, name='fav-course'),
    path('list-fav-courses/', list_fav_course, name='list-fav-course'),
    path('remove-fav-courses/<int:pk>', remove_fav_courses, name='remove-fav-course'),

    path('enrolled-courses/', EnrolledCoursesView.as_view(), name='fav-course'),
    path('uploaded-courses/', my_uploaded_course, name='uploaded-course'),


    path('search/', search_view, name='search'),

]

