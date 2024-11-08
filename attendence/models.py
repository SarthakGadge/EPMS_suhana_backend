from django.db import models
from django.db import models
from django.conf import settings
from django.utils import timezone
from userauth.models import Employee


class AttendanceRecord(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='Absent')
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'attendance_record'
        unique_together = ('employee', 'date')

    def __str__(self):
        return f"{self.employee.username} - {self.date} - {self.status}"
