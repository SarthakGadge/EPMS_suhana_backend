from rest_framework import serializers
from userauth.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['employee_id', 'user', 'contact_number', 'joining_date', 'full_name',
                  'profile_image', 'gender', 'emergency_contact', 'dob']
