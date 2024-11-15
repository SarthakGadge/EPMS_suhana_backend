from django.db import models
from userauth.models import Manager, Employee


class AdminFeedbackManager(models.Model):
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    rating = models.FloatField()
    feedback = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.manager} - Rating: {self.rating}"


class AdminFeedbackEmployee(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    rating = models.FloatField()
    feedback = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee} - Rating: {self.rating}"
