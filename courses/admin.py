from django.contrib import admin

# Register your models here.
from courses.models.courses import CourseModel, FavCoursesModel, EnrolledCoursesModel, RatingCoursesModel, ModuleModel, \
    LessonsModel
from courses.models.categories import CategoriesModel, SubCategoriesModel
from courses.models.comments import CommentsModel

admin.site.register(FavCoursesModel)
admin.site.register(CategoriesModel)
admin.site.register(SubCategoriesModel)
admin.site.register(CommentsModel)
admin.site.register(EnrolledCoursesModel)
admin.site.register(RatingCoursesModel)


@admin.register(CourseModel)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "subcategory",
        "course_owner",
        "price",
        "is_valid"
    )


@admin.register(ModuleModel)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("name", "course")


@admin.register(LessonsModel)
class LessonsAdmin(admin.ModelAdmin):
    list_display = ("name", "module")
