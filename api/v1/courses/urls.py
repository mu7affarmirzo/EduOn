from django.urls import path, include
from api.v1.courses.views import *

app_name = 'courses'

urlpatterns = [
    path('', CoursesListView.as_view(), name='courses'),
    path('<int:pk>', CoursesDetailView.as_view(), name='courses-detail'),
    path('subcategories/', SubCategoriesListView.as_view(), name='sub-categories'),
    path('subcategories/<int:pk>', SubCategoriesDetailView.as_view(), name='sub-categories-detail'),
    path('categories/', CategoriesListView.as_view(), name='categories'),
    path('categories/<int:pk>', CategoriesDetailView.as_view(), name='categories-detail'),

    path('comments/', CommentsListView.as_view(), name='comments'),
    path('comments/<int:pk>', CommentsDetailView.as_view(), name='comments-detail'),

    path('fav-courses/', post_fav_course, name='fav-course'),
    path('list-fav-courses/', list_fav_course, name='list-fav-course'),
    path('remove-fav-courses/<int:pk>', remove_fav_courses, name='remove-fav-course'),
    # path('fav-courses-list', list_my_fav_courses, name='fav-course-list'),
]

