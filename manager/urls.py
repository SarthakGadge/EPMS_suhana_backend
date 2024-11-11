from django.urls import path

from manager.views import ManagerCreateView

urlpatterns = [
    path('manager_profile/', ManagerCreateView.as_view(), name='resend-otp'),
    path('manager_profile/<int:manager_id>/',
         ManagerCreateView.as_view(), name='manager-delete'),
]
