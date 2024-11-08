from rest_framework import viewsets, permissions
from django.db.models import Q
from .models import Feedback
from .serializers import FeedbackSerializer

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()  
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
      
        user = self.request.user
        return Feedback.objects.filter(Q(to_user=user) | Q(from_user=user))

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)
