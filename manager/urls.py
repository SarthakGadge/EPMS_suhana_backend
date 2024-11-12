from django.urls import path

from manager.views import ManagerCreateView, ManagerFeedbackCreateView

urlpatterns = [
    path('manager_profile/', ManagerCreateView.as_view(), name='resend-otp'),
    path('manager_profile/<int:manager_id>/',
         ManagerCreateView.as_view(), name='manager-delete'),
    path('manager_feedback/', ManagerFeedbackCreateView.as_view(),
         name='create_performance_goal'),
]
