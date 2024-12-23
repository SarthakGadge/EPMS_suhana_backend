from django.urls import path
from .views import CreateUserView, AdminUpdateView, AdminFeedbacktoManager, AdminFeedbacktoEmployee, GetAllFeedback

urlpatterns = [
    path('create_user/', CreateUserView.as_view(), name='create-user'),
    path('admin/update/', AdminUpdateView.as_view(), name='admin-update'),
    path('admin_manager/', AdminFeedbacktoManager.as_view(), name='admin-update'),
    path('admin_employee/', AdminFeedbacktoEmployee.as_view(), name='admin-update'),
    path('manager_employee_feedback/',
         GetAllFeedback.as_view(), name='admin-update')
]
