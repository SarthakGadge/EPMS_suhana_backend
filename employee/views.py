from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from userauth.models import Employee
from .serializers import EmployeeSerializer
from django.shortcuts import get_object_or_404
from attendence.models import AttendanceRecord


class EmployeeView(APIView):
    def get(self, request):
        role = request.user.role
        id = request.user.id

        if role == "employee":
            employee = get_object_or_404(Employee, user_id=id)
            serializer = EmployeeSerializer(employee)

        elif role == "manager" or role == "admin":
            employees = Employee.objects.all()
            serializer = EmployeeSerializer(employees, many=True)
        else:
            return Response({"You dont have access to this"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST request: Create a new employee
    def post(self, request):
        if request.user.role != "employee":
            return Response({"You dont have access to this"}, status=status.HTTP_401_UNAUTHORIZED)

        id = request.user.id

        if Employee.objects.filter(user_id=id).exists():
            return Response({"msg": "Employee record already exists for this user."},
                            status=status.HTTP_400_BAD_REQUEST)
        # Create a copy to avoid modifying the original request data
        data = request.data.copy()
        data['user'] = id        # Add user_id to the data

        serializer = EmployeeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PATCH request: Update an existing employee by ID
    def patch(self, request, employee_id=None):
        if not request.user.role == "employee":
            return Response({"You dont have access to this"}, status=status.HTTP_401_UNAUTHORIZED)
        employee = get_object_or_404(Employee, employee_id=employee_id)
        serializer = EmployeeSerializer(
            employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE request: Delete an employee by ID
    def delete(self, request, employee_id=None):
        if not request.data.role == "employee":
            return Response({"You dont have access to this"}, status=status.HTTP_401_UNAUTHORIZED)
        employee = get_object_or_404(Employee, employee_id=employee_id)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
