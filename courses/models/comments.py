from django.db import models

from accounts.models import Account
from courses.models.courses import CourseModel


class CommentsModel(models.Model):
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True)
    course = models.ForeignKey(CourseModel, related_name="comments", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author.id}-{self.course.id}-{self.date_created.date()}"

    class Meta:
        ordering = ('-date_created',)

