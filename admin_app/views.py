from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils.crypto import get_random_string
from .serializers import CreateUserSerializer
from userauth.utils import user_creation_and_welcome
from .serializers import AdminSerializer
from rest_framework.exceptions import NotFound
from userauth.models import Admin


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
