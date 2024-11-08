from rest_framework import serializers
from .models import CustomUser, Admin, Employee, Manager

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role']

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['contact_number','full_name','joining_date','profile_image','gender','emergency_contact','dob']