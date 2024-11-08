from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AttendanceRecord
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import AttendanceRecord
from userauth.models import Employee


class AnnualAttendanceRateView(APIView):
    def get(self, request, year):
        # Define the start and end dates for the specified year
        start_date = timezone.datetime(year, 1, 1)
        end_date = timezone.datetime(year, 12, 31)

        # Query attendance records within the specified year
        attendance_records = AttendanceRecord.objects.filter(
            date__range=(start_date, end_date))

        # Count total attendance days and present days across all employees
        total_days = attendance_records.count()
        present_days = attendance_records.filter(status='Present').count()

        # Calculate overall annual attendance rate
        if total_days > 0:
            attendance_rate = (present_days / total_days) * 100
        else:
            attendance_rate = 0.0  # To handle cases where there are no records

        # Return the overall attendance rate as JSON
        return Response({'annual_attendance_rate': attendance_rate})


class EmpStats(APIView):

    def get(self, request, date=None):

        role = request.user.role
        if not role in ['admin', 'manager']:
            return Response({"You dont have access to this"}, status=status.HTTP_401_UNAUTHORIZED)

        emp = Employee.objects.count()

        if date:
            try:
                # Parse the date string in 'YYYY-MM-DD' format
                target_date = timezone.datetime.strptime(
                    date, '%Y-%m-%d').date()
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Default to today's date if no date is provided
            target_date = timezone.now().date()

        # Count the number of present employees for the target date
        present_count = AttendanceRecord.objects.filter(
            date=target_date, status='Present').count()

        return Response({"date": target_date,
                         "total_present_employees": present_count,
                         "Total_emp": emp,
                         "Emp_on_leave": emp-present_count
                         }, status=status.HTTP_200_OK)
