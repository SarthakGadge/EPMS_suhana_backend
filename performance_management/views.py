from .serializers import SelfEvaluationSerializer
from .models import PerformanceEvaluation, Goal
from rest_framework import viewsets
from .models import Department, Role, Goal, PerformanceEvaluation, PerformanceReview, Feedback, Training, EmployeeTraining, Notification
from .serializers import PerformanceEvaluation
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from userauth.models import Employee
from .models import Goal
from userauth.models import Manager
from django.db import connection
from .models import Training

from .serializers import (
    DepartmentSerializer,
    RoleSerializer,
    GoalSerializer,
    PerformanceEvaluationSerializer,
    PerformanceReviewSerializer,
    FeedbackSerializer,
    TrainingSerializer,
    EmployeeTrainingSerializer,
    NotificationSerializer,
    ManagerEvaluationSerializer
)


# Department ViewSet
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


# Role ViewSet
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


# Goal ViewSet
class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer


# PerformanceEvaluation ViewSet

# Feedback ViewSet
class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


# Training ViewSet
class TrainingViewSet(viewsets.ModelViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer


# EmployeeTraining ViewSet
class EmployeeTrainingViewSet(viewsets.ModelViewSet):
    queryset = EmployeeTraining.objects.all()
    serializer_class = EmployeeTrainingSerializer


# Notification ViewSet
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class PerformanceEvaluationView(APIView):
    def post(self, request):
        role = request.user.role
        print(role)
        if not role == 'employee':
            return Response({"msg": "You are unauthorized to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
        id = request.user.id
        employee = get_object_or_404(Employee, id=id)
        return Response(employee.id)


class SelfEvaluationView(APIView):
    def get(self, request):
        # if request.user.role == 'admin':
        #     return Response({"msg": "You are unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        eval_instance = PerformanceEvaluation.objects.all()
        serializer = PerformanceEvaluationSerializer(eval_instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        role = request.user.role
        if not role == 'employee':
            return Response("You are unauthorized", status=status.HTTP_401_UNAUTHORIZED)
        # Validate and parse input data using the serializer
        user_id = request.user.id

        # Retrieve the Employee object for this user_id
        employee = get_object_or_404(Employee, user_id=user_id)

        # Validate and parse input data using the serializer
        serializer = SelfEvaluationSerializer(data=request.data)

        if serializer.is_valid():
            # Check if the provided goal exists
            goal = serializer.validated_data['goal']

            # Ensure an evaluation for this goal and employee exists or create it
            evaluation, created = PerformanceEvaluation.objects.get_or_create(
                employee=employee.user,  # Set the employee's user here
                goal=goal,
                defaults={
                    'self_rating': serializer.validated_data['self_rating']}
            )

            # Update the self-rating if it already exists
            if not created:
                evaluation.self_rating = serializer.validated_data['self_rating']
                evaluation.save()

            return Response(
                {"message": "Self-evaluation submitted successfully."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, evaluation_id):
        # Check if the user is a manager (for example, assume 'is_manager' field or role in request)
        if not request.user.role == 'manager':
            return Response({"msg": "Only managers are allowed to perform this action."},
                            status=status.HTTP_403_FORBIDDEN)

        # Retrieve the evaluation based on the ID and verify existence
        user_id = request.user.id
        # print('idhar')
        # print(user_id)
        manager = get_object_or_404(Manager, user_id=user_id)
        evaluation = get_object_or_404(PerformanceEvaluation, id=evaluation_id)
        # if not evaluation.self_rating:
        #     return Response({"error": "Self-rating must be completed by the employee before manager can evaluate."},
        #                     status=status.HTTP_400_BAD_REQUEST)

        serializer = ManagerEvaluationSerializer(
            evaluation, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(manager_id=manager)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TrainingView(APIView):
    def post(self, request):
        if request.user.role != 'manager':
            return Response({"msg": "You are unauthorized to perform this action."}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = request.user.id

        updated_request = request.data.copy()

        try:
            manager = Manager.objects.get(user_id=request.user.id)
        except Manager.DoesNotExist:
            return Response({"msg": "Manager not found."}, status=status.HTTP_400_BAD_REQUEST)

        updated_request['manager'] = manager.manager_id

        employee = request.data.get('employee_id')

        if not employee:
            return Response({"msg": "employee id is required."}, status=status.HTTP_400_BAD_REQUEST)

        updated_request['employee'] = employee

        serializer = TrainingSerializer(data=updated_request)

        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Training has successfully been assigned."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        role = request.user.role
        # Get the search query for 'name' from the URL
        name_filter = request.GET.get('name', '')

        try:
            if role == 'employee':
                user_id = request.user.id
                emp_id = Employee.objects.get(user_id=user_id)
                instance = Training.objects.filter(employee_id=emp_id)

            elif role == 'manager':
                user_id = request.user.id
                manager_id = Manager.objects.get(user_id=user_id)
                instance = Training.objects.filter(manager_id=manager_id)

            elif role == 'admin':
                instance = Training.objects.all()

            else:
                return Response({"msg": "Unauthorized access."}, status=status.HTTP_401_UNAUTHORIZED)

            # If a 'name' parameter is provided, filter by the name
            if name_filter:
                # Case-insensitive search
                instance = instance.filter(name__icontains=name_filter)

            serializer = TrainingSerializer(instance, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, pk):
        if request.user.role != "manager":
            return Response({"msg": "You are unauthorized"}, status=status.HTTP_200_OK)

        try:
            # Get the training instance by primary key
            training = Training.objects.get(pk=pk)
        except Training.DoesNotExist:
            return Response({"msg": "Training not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = TrainingSerializer(
            training, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if request.user.role != "manager":
            return Response({"msg": "You are unauthorized"}, status=status.HTTP_200_OK)
        try:
            # Get the training instance by primary key
            training = Training.objects.get(pk=pk)
        except Training.DoesNotExist:
            return Response({"msg": "Training not found."}, status=status.HTTP_404_NOT_FOUND)
        training.delete()

        # Return a success response
        return Response({"msg": "Training has been successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
