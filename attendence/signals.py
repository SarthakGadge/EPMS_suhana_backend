from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from .models import AttendanceRecord
from django.contrib.auth.models import User


@receiver(user_logged_in)
def log_attendance(sender, request, user, **kwargs):
    today = timezone.now().date()
    # Get or create the attendance record for the current day
    attendance, created = AttendanceRecord.objects.get_or_create(
        # Assuming 'employee_profile' related name on the User model
        employee=user.employee_profile,
        date=today,
        defaults={'status': 'Present', 'check_in_time': timezone.now()}
    )

    # If record already exists, update the check-in time (in case of repeated logins)
    if not created:
        attendance.check_in_time = timezone.now()
        attendance.status = 'Present'  # Optional: you can check if this status is needed
        attendance.save()
