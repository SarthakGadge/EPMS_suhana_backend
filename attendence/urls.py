from django.urls import path
from .views import AnnualAttendanceRateView, EmpStats

urlpatterns = [
    path('annual_attendance_rate/<int:year>/',
         AnnualAttendanceRateView.as_view(), name='annual-attendance-rate'),
    path("emp_stats/", EmpStats.as_view(), name="emp data"),
    path("emp_stats/<str:date>/", EmpStats.as_view(), name="emp data"),

]
