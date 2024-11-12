from django.db import models
from userauth.models import Employee, Manager


class ManagerFeedback(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    rating = models.IntegerField()
    feedback = models.TextField()
    manager = models.ForeignKey(
        Manager, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"
