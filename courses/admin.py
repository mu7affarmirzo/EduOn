from django.contrib import admin

# Register your models here.
from courses.models.courses import CourseModel, FavCoursesModel
from courses.models.categories import CategoriesModel, SubCategoriesModel
from courses.models.comments import CommentsModel

admin.site.register(CourseModel)
admin.site.register(FavCoursesModel)
admin.site.register(CategoriesModel)
admin.site.register(SubCategoriesModel)
admin.site.register(CommentsModel)