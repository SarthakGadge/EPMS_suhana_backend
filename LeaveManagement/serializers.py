from rest_framework import serializers
from .models import Leave

class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = [
            'employee', 'leave_type', 'start_date', 'end_date', 
            'reason', 'status', 'applied_on', 'manager_approval_date', 
            'admin_approval_date', 'duration'
        ]
        read_only_fields = ['employee', 'status', 'applied_on', 'manager_approval_date', 'admin_approval_date', 'duration']

    def validate(self, data):
        # Ensure start_date is before or equal to end_date
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("End date must be after start date.")

        # Check for overlapping leaves
        user = self.context['request'].user
        if Leave.objects.filter(
            employee=user,
            start_date__lte=data['end_date'],
            end_date__gte=data['start_date'],
            status__in=['Pending', 'Manager Approved', 'Admin Approved']
        ).exists():
            raise serializers.ValidationError("You already have a leave in this period.")
        
        return data
class LeaveApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = ['status']