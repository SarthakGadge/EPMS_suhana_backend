from django.db import models
from django.conf import settings
from django.utils import timezone

from django.core.exceptions import ValidationError

class Leave(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('Sick', 'Sick'),
        ('Casual', 'Casual'),
        ('Maternity', 'Maternity'),
        ('Paternity', 'Paternity'),
        ('Other', 'Other'),
    ]

    LEAVE_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Manager Approved', 'Manager Approved'),
        ('Admin Approved', 'Admin Approved'),
        ('Rejected', 'Rejected'),
        ('Cancelled', 'Cancelled'),
    ]

    employee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='leaves', on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=LEAVE_STATUS_CHOICES, default='Pending')
    applied_on = models.DateTimeField(auto_now_add=True)
    manager_approval_date = models.DateTimeField(null=True, blank=True)
    admin_approval_date = models.DateTimeField(null=True, blank=True)
    duration = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.employee.email} - {self.leave_type} ({self.status})"

    @property
    def leave_duration(self):
        return (self.end_date - self.start_date).days + 1

    def save(self, *args, **kwargs):
        # Calculate leave duration before saving
        if self.start_date and self.end_date:
            self.duration = self.leave_duration

        # Check for overlapping leaves
        if Leave.objects.filter(
                employee=self.employee,
                start_date__lte=self.end_date,
                end_date__gte=self.start_date,
                status__in=['Pending', 'Manager Approved', 'Admin Approved']).exists():
            raise ValidationError("You already have an approved or pending leave in this period.")
        
        super().save(*args, **kwargs)
