# LeaveManagement/urls.py
from django.urls import path
from .views import LeaveViewSet, ManagerLeaveApprovalView, AdminLeaveApprovalView

urlpatterns = [
    path('', LeaveViewSet.as_view({'get': 'list', 'post': 'create'}), name='leave-list'),
    path('<int:pk>/', LeaveViewSet.as_view({'get': 'retrieve'}), name='leave-detail'),
    path('<int:pk>/manager-approve/', ManagerLeaveApprovalView.as_view(), name='manager-approve-leave'),
    path('<int:pk>/admin-approve/', AdminLeaveApprovalView.as_view(), name='admin-approve-leave'),
]
