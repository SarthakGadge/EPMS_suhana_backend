from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils.crypto import get_random_string
from .serializers import CreateUserSerializer, AdmintoEmployeeFeedbackSerializer, AdmintoManagerFeedbackSerializer
from userauth.utils import user_creation_and_welcome
from .serializers import AdminSerializer
from rest_framework.exceptions import NotFound
from userauth.models import Admin
from .models import AdminFeedbackEmployee, AdminFeedbackManager
from django.db import connection
from userauth.RolePermission import IsAdmin


class CreateUserView(APIView):
    def post(self, request):
        user_role = request.user.role

        # Only allow superadmin and admin to create users
        if user_role not in ['admin']:
            return Response({"msg": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        if not request.data.get('email'):
            return Response({"msg": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        if not request.data.get('username'):
            return Response({"msg": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)

        if not request.data.get('role'):
            return Response({"msg": "Role is required."}, status=status.HTTP_400_BAD_REQUEST)

        if request.data.get('role') not in ['manager', 'employee']:
            return Response({"msg": "Please enter a valid role."}, status=status.HTTP_403_FORBIDDEN)

        temp_password = get_random_string(length=8)
        # Add the generated password to the request data
        request.data['password'] = temp_password
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            user_creation_and_welcome(user, temp_password)

            return Response({'message': 'User created successfully, an email has been sent to the user.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminUpdateView(APIView):
    def get(self, request):
        if request.user.role != 'admin':
            return Response({"msg": "You are unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        admin_instance = Admin.objects.all()
        serializer = AdminSerializer(admin_instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_object(self):
        try:
            return Admin.objects.get()
        except Admin.DoesNotExist:
            raise NotFound("Admin not found.")

    def patch(self, request, *args, **kwargs):
        admin = self.get_object()
        serializer = AdminSerializer(admin, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminFeedbacktoEmployee(APIView):
    def get(self, request):
        instance = AdminFeedbackEmployee.objects.all()
        serializer = AdmintoEmployeeFeedbackSerializer(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AdmintoEmployeeFeedbackSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Feedback given successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminFeedbacktoManager(APIView):
    def get(self, request):
        instance = AdminFeedbackManager.objects.all()
        serializer = AdmintoManagerFeedbackSerializer(instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AdmintoManagerFeedbackSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Feedback given successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllFeedback(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        try:
            all_data = {}  # Store results from both tables

            with connection.cursor() as cursor:
                # Fetch data from manager_managerfeedback
                cursor.execute("SELECT * FROM manager_managerfeedback")
                columns = [col[0] for col in cursor.description]
                manager_feedback = [dict(zip(columns, row))
                                    for row in cursor.fetchall()]
                all_data["manager_feedback_to_employee"] = manager_feedback

                # Fetch data from feedback_feedback
                cursor.execute("SELECT * FROM feedback_feedback")
                columns = [col[0] for col in cursor.description]
                feedback_data = [dict(zip(columns, row))
                                 for row in cursor.fetchall()]
                all_data["employee_feedback_to_manager"] = feedback_data

            return Response(all_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
