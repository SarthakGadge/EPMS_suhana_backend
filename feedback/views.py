import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.db import connection, IntegrityError, transaction
from django.http import JsonResponse
from rest_framework import viewsets, permissions
from django.db.models import Q
from .models import Feedback
from .serializers import FeedbackSerializer
from django.shortcuts import get_object_or_404
from userauth.models import Employee
from rest_framework.response import Response


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        user = self.request.user
        return Feedback.objects.filter(Q(to_user=user) | Q(from_user=user))

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        user = self.request.user
        return Feedback.objects.filter(Q(to_user=user) | Q(from_user=user))

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)


@method_decorator(csrf_exempt, name='dispatch')
class FeedbackCreateView(APIView):
    def post(self, request):
        try:
            # Parse JSON payload
            data = json.loads(request.body)
            # "Self Feedback" or "Manager Feedback"
            feedback_type = data.get("feedback_type")

            # If only "Manager Feedback" type is provided, return list of managers
            if feedback_type == "Manager Feedback" and len(data) == 1:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT user_id, full_name FROM Manager")
                    managers = cursor.fetchall()

                # Format data as a list of dictionaries
                manager_list = [
                    {"user_id": manager[0], "full_name": manager[1]} for manager in managers]
                return JsonResponse({"managers": manager_list}, status=200)

            # Continue with feedback creation if all fields are provided
            feedback_text = data.get("feedback_text")
            rating = data.get("rating")
            from_id = request.user.id
            from_user_id = Employee.objects.get(user_id=from_id)

            to_user_id = data.get(
                "manager_id") if feedback_type == "Manager Feedback" else from_user_id
            anonymous = data.get("anonymous", 0)

            # Validate required fields
            if not all([feedback_type, feedback_text, rating, from_user_id]):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            # Check feedback type validity
            if feedback_type not in ["Self Feedback", "Manager Feedback"]:
                return JsonResponse({"error": "Invalid feedback type, must be 'Self Feedback' or 'Manager Feedback'"}, status=400)

            # Validate the rating (e.g., between 1 and 5)
            if not (1 <= rating <= 5):
                return JsonResponse({"error": "Rating must be between 1 and 5"}, status=400)

            # If it's manager feedback, validate to_user_id and retrieve manager's full name
            # manager_name = None
            if feedback_type == "Manager Feedback":
                if not to_user_id:
                    return JsonResponse({"error": "Manager selection is required for manager feedback"}, status=400)

            if feedback_type == "Self Feedback":
                to_user_id = None

                # Retrieve manager's full name from the Manager table
                # with connection.cursor() as cursor:
                #     cursor.execute("""
                #         SELECT full_name
                #         FROM Manager
                #         WHERE user_id = %s
                #     """, [to_user_id])
                #     result = cursor.fetchone()

                #     if not result:
                #         return JsonResponse({"error": "Manager not found"}, status=404)

            # manager_name =

            # Insert data into feedback_feedback table
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO feedback_feedback 
                        (feedback_text, feedback_type, employee_id, manager_id, rating, anonymous, created_at)
                        VALUES (%s, %s, %s, %s, %s, %s, NOW())
                    """, [feedback_text, feedback_type, from_user_id.employee_id, to_user_id, rating, anonymous])

            response_message = (
                "Self-feedback submitted successfully" if feedback_type == "Self Feedback"
                else f"Feedback for manager submitted successfully"
            )
            return JsonResponse({"message": response_message}, status=201)

        except IntegrityError as e:
            return JsonResponse({"error": f"Failed to create feedback due to integrity error: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class ManagerListView(APIView):
    def get(self, request):
        try:
            # Retrieve the list of managers from the Manager table
            with connection.cursor() as cursor:
                cursor.execute("SELECT user_id, full_name FROM Manager")
                managers = cursor.fetchall()

            # Format data as a list of dictionaries
            manager_list = [{"user_id": manager[0],
                             "full_name": manager[1]} for manager in managers]

            return JsonResponse({"managers": manager_list}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
