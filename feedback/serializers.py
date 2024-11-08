from rest_framework import serializers
from .models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['from_user', 'to_user', 'feedback_text', 'feedback_type', 'anonymous', 
                  'rating', 'title', 'department', 'feedback_status', 'response']
        read_only_fields = ['from_user', 'created_at']  
