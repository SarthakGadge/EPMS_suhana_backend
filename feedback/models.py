from django.db import models
from django.conf import settings


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
    
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='feedback_given', on_delete=models.CASCADE)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='feedback_received', on_delete=models.CASCADE)
    feedback_text = models.TextField()
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPES)
    anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Additional fields
    rating = models.IntegerField(null=True, blank=True)  # Rating from 1 to 5
    title = models.CharField(max_length=100, blank=True)  # Short title or subject for the feedback
    department = models.CharField(max_length=100, blank=True)  # Optional department field
    # goal_association = models.ForeignKey('Goal', null=True, blank=True, on_delete=models.SET_NULL)  #  you have a Goal model
    feedback_status = models.CharField(max_length=20, choices=[
        ('Acknowledged', 'Acknowledged'),
        ('Pending', 'Pending'),
        ('Responded', 'Responded'),
    ], default='Pending')
    response = models.TextField(blank=True, null=True)  # Allow managers to respond to feedback

    def __str__(self):
        return f"Feedback from {self.from_user.email} to {self.to_user.email} ({self.feedback_type})"

