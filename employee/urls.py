from django.urls import path
from .views import EmployeeView

urlpatterns = [
    path('employees/', EmployeeView.as_view(),
         name='employee-list-create'),        # For GET all and POST
    path('employees/<int:employee_id>/', EmployeeView.as_view(),
         name='employee-detail'),  # For GET single, PATCH, and DELETE
]
