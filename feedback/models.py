from django.db import models
from django.conf import settings
from userauth.models import Manager, Employee


# models.py
from django.db import models
from django.conf import settings


class Feedback(models.Model):
    FEEDBACK_TYPES = [
        ('Direct Report', 'Direct Report'),
        ('Employee to Admin', 'Employee to Admin'),
        ('Employee to Manager', 'Employee to Manager'),
        ('Manager to admin', 'Manager to admin'),
        ('Manager to Employee', 'Manager to Employee'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    manager = models.ForeignKey(
        Manager, on_delete=models.CASCADE, null=True, blank=True)
    feedback_text = models.TextField()
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES)
    anonymous = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Additional fields
    # Rating from 1 to 5
    rating = models.IntegerField(null=True, blank=True)
    # Short title or subject for the feedback
    title = models.CharField(max_length=100, blank=True, null=True)
    # Optional department field
    department = models.CharField(max_length=100, blank=True, null=True)
    # goal_association = models.ForeignKey('Goal', null=True, blank=True, on_delete=models.SET_NULL)  #  you have a Goal model
    feedback_status = models.CharField(max_length=20, null=True, choices=[
        ('Acknowledged', 'Acknowledged'),
        ('Pending', 'Pending'),
        ('Responded', 'Responded'),
    ], default='Pending')
    # Allow managers to respond to feedback
    response = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Feedback from {self.from_user.email} to {self.to_user.email} ({self.feedback_type})"
