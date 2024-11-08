from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('userauth.urls')),
    path('api/', include('feedback.urls')),
    path('api/', include('PerformanceReview.urls')),
    path('api/', include('LeaveManagement.urls')),
    path('api/', include('performance_management.urls')),
    path('api/', include('admin_app.urls')),
    path('api/', include('attendence.urls')),
    path('api/', include('employee.urls')),

]
