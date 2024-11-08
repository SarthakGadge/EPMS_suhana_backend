from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('manager', 'manager'),
        ('admin', 'admin'),
        ('employee', 'employee'),
    )

    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default='employee')
    email = models.EmailField(unique=True)  # Ensure email is unique
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)
    max_otp_try = models.IntegerField(default=3)
    otp_max_out = models.DateTimeField(null=True, blank=True)
    password_reset_otp = models.CharField(max_length=6, null=True, blank=True)
    password_reset_otp_expiry = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'  # Use email as the username field
    REQUIRED_FIELDS = ['username']  # Remove email from REQUIRED_FIELDS

    def __str__(self):
        return self.email

    def is_otp_valid(self):
        if self.otp and self.otp_expiry:
            return timezone.now() <= self.otp_expiry
        return False

    def can_send_otp(self):
        if self.otp_max_out:
            return timezone.now() > self.otp_max_out
        return self.max_otp_try > 0


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='admin_profile')
    full_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    joining_date = models.DateField()
    profile_image = models.ImageField(
        upload_to='admin_profiles/', blank=True, null=True)
    gender = models.CharField(max_length=10)
    emergency_contact = models.CharField(max_length=15)
    dob = models.DateField()

    class Meta:
        db_table = 'admin'

    def save(self, *args, **kwargs):
        # Check if an Admin instance already exists
        if not self.pk and Admin.objects.exists():
            raise ValidationError("Only one admin instance is allowed.")
        super().save(*args, **kwargs)


class Manager(models.Model):
    manager_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='manager_profile')
    contact_number = models.CharField(max_length=15)
    joining_date = models.DateField()
    profile_image = models.ImageField(
        upload_to='manager_profiles/', blank=True, null=True)
    gender = models.CharField(max_length=10)  # Add max_length for gender
    employees_supervised = models.ManyToManyField(
        'Employee', related_name='managers', blank=True)
    emergency_contact = models.CharField(max_length=15)
    dob = models.DateField()

    class Meta:
        db_table = 'manager'


class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employee_profile')
    contact_number = models.CharField(max_length=15)
    joining_date = models.DateField()
    full_name = models.CharField(max_length=100)
    profile_image = models.ImageField(
        upload_to='employee_profiles/', blank=True, null=True)
    gender = models.CharField(max_length=10)  # Add max_length for gender
    emergency_contact = models.CharField(max_length=15)
    dob = models.DateField()

    class Meta:
        db_table = 'employee'
