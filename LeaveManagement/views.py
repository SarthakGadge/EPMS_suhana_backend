from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, generics
from rest_framework.response import Response
from django.utils import timezone
from .models import Leave
from .serializers import LeaveSerializer, LeaveApprovalSerializer
from .permissions import IsEmployee, IsManager, IsAdmin

class LeaveViewSet(viewsets.ModelViewSet):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    permission_classes = [IsAuthenticated, IsEmployee]  # Employee permission here

    def get_queryset(self):
        # Employees can only see their own leave applications
        user = self.request.user
        if user.role == 'employee':
            return Leave.objects.filter(employee=user)
        return Leave.objects.none()  # Restrict other roles

    def perform_create(self, serializer):
        # Automatically set the employee to the current user when applying for leave
        serializer.save(employee=self.request.user)


class ManagerLeaveApprovalView(generics.UpdateAPIView):
    queryset = Leave.objects.filter(status='Pending')  # Only show pending leaves
    serializer_class = LeaveApprovalSerializer
    permission_classes = [IsAuthenticated, IsManager]  # Manager permission here

    def get_queryset(self):
        user = self.request.user
        if user.role == 'manager':
            return Leave.objects.filter(employee__employee_profile__managers=user.manager_profile)
        return Leave.objects.none()

    def update(self, request, *args, **kwargs):
        leave = self.get_object()
        action = request.data.get('action')

        if action == 'approve':
            leave.status = 'Manager Approved'
            leave.manager_approval_date = timezone.now()
        elif action == 'reject':
            leave.status = 'Rejected'
            leave.manager_approval_date = timezone.now()
        else:
            return Response({"error": "Invalid action"}, status=400)

        leave.save()
        return Response({"message": f"Leave successfully {action}ed"}, status=200)


class AdminLeaveApprovalView(generics.UpdateAPIView):
    queryset = Leave.objects.filter(status='Manager Approved')  # Show only manager-approved leaves
    serializer_class = LeaveApprovalSerializer
    permission_classes = [IsAuthenticated, IsAdmin]  # Admin permission here

    def update(self, request, *args, **kwargs):
        leave = self.get_object()
        action = request.data.get('action')

        if action == 'approve':
            leave.status = 'Admin Approved'
            leave.admin_approval_date = timezone.now()
        elif action == 'reject':
            leave.status = 'Rejected'
            leave.admin_approval_date = timezone.now()
        else:
            return Response({"error": "Invalid action"}, status=400)

        leave.save()
        return Response({"message": f"Leave successfully {action}ed by admin"}, status=200)
