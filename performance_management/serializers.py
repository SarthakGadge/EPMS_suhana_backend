from rest_framework import serializers
from .models import Department, PerformanceEvaluation, Role, Goal, Feedback, Training, EmployeeTraining, Notification, PerformanceReview


from rest_framework import serializers
from .models import PerformanceEvaluation, Goal


class SelfEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceEvaluation
        # Only include fields the employee can modify
        fields = ['goal', 'self_rating']

    def validate_self_rating(self, value):
        # Example validation to ensure rating is between 1 and 5
        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "Self rating must be between 1 and 5.")
        return value

    def validate_goal(self, value):
        if not Goal.objects.filter(id=value.id).exists():
            raise serializers.ValidationError(
                "The provided goal ID does not exist.")
        return value


class ManagerEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceEvaluation
        fields = ['manager_rating', 'final_rating',
                  'manager_feedback', 'manager_id']

# Department Serializer


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        ref_name = 'DepartmentSerializer'

# Role Serializer


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
        ref_name = 'RoleSerializer'

# Goal Serializer


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'
        ref_name = 'GoalSerializer'

# PerformanceEvaluation Serializer


class PerformanceEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceEvaluation
        fields = '__all__'
        ref_name = 'PerformanceEvaluationSerializer'

# PerformanceReview Serializer


class PerformanceReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceReview
        fields = '__all__'
        ref_name = 'PerformanceReviewSerializer'

# Feedback Serializer


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
        ref_name = 'FeedbackSerializer'

# Training Serializer


class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = '__all__'
        ref_name = 'TrainingSerializer'

# EmployeeTraining Serializer


class EmployeeTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeTraining
        fields = '__all__'
        ref_name = 'EmployeeTrainingSerializer'

# Notification Serializer


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        ref_name = 'NotificationSerializer'
