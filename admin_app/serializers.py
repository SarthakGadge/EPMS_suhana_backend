from userauth.models import CustomUser, Admin
from rest_framework import serializers
from .models import AdminFeedbackEmployee, AdminFeedbackManager
from django.core.exceptions import ValidationError
from rest_framework import status


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = [
            'full_name', 'contact_number', 'joining_date', 'profile_image',
            'gender', 'emergency_contact', 'dob'
        ]

    def update(self, instance, validated_data):
        # You can perform any custom logic here if needed before saving
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class AdmintoManagerFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminFeedbackManager
        fields = '__all__'

    def validate_rating(self, value):
        if value > 5:  # Adjusted to ensure the rating is not more than 5
            raise ValidationError({"msg": "The rating can't be more than 5."})
        return value  # Return the valid rating


class AdmintoEmployeeFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminFeedbackEmployee
        fields = '__all__'

    def validate_rating(self, value):
        if value > 5:  # Same adjustment here
            raise ValidationError({"msg": "The rating can't be more than 5."})
        return value  # Return the va
