from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import PerformanceReview
from .serializers import PerformanceReviewSerializer

class PerformanceReviewViewSet(viewsets.ModelViewSet):
    queryset = PerformanceReview.objects.all()
    serializer_class = PerformanceReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically assign the current user as the employee
        serializer.save(employee=self.request.user)

    def get_queryset(self):
        # Limit the queryset to the current user's performance reviews
        return self.queryset.filter(employee=self.request.user)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        # Approve the performance review
        review = self.get_object()
        review.is_approved = True
        review.save()
        return Response({'status': 'review approved'})

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        # Submit the performance review
        review = self.get_object()
        review.status = 'Submitted'
        review.save()
        return Response({'status': 'review submitted'})

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        # Mark the performance review as completed
        review = self.get_object()
        review.status = 'Completed'
        review.save()
        return Response({'status': 'review completed'})
