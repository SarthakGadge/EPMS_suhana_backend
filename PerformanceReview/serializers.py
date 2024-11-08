from rest_framework import serializers
from .models import PerformanceReview


class PerformanceReviewSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.username', read_only=True)
    manager_name = serializers.CharField(source='manager.username', read_only=True)

    class Meta:
        model = PerformanceReview
        fields = [
            'employee', 'employee_name', 'manager', 'manager_name', 'title', 
            'description', 'deadline', 'self_rating', 'manager_rating', 
            'is_approved', 'attachment', 'review_cycle', 'status', 'created_at'
        ]
        read_only_fields = ['employee', 'created_at', 'employee_name', 'manager_name']

    # Validate self rating to be between 1 and 5
    def validate_self_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Self rating must be between 1 and 5.")
        return value

    # Validate manager rating to be between 1 and 5
    def validate_manager_rating(self, value):
        if value and (value < 1 or value > 5):
            raise serializers.ValidationError("Manager rating must be between 1 and 5.")
        return value
