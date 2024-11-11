from django.http import JsonResponse
from django.db import connection, IntegrityError, transaction
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status
import json
from userauth.models import Manager
from .serializers import ManagerSerializer
from rest_framework.response import Response


@method_decorator(csrf_exempt, name='dispatch')
class ManagerCreateView(APIView):

    def get(self, request):
        manager_instance = Manager.objects.all()
        serializer = ManagerSerializer(manager_instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            # Ensure the user is authenticated and retrieve the user ID
            if not request.user.is_authenticated:
                return JsonResponse({"error": "User not authenticated"}, status=401)

            user_id = request.user.id  # Get the user ID from the authenticated user

            # Parse the incoming JSON payload
            data = json.loads(request.body)

            # Extract manager profile details from the request body
            full_name = data.get("full_name")
            contact_number = data.get("contact_number")
            joining_date = data.get("joining_date")
            profile_image = data.get("profile_image")
            gender = data.get("gender")
            emergency_contact = data.get("emergency_contact")
            dob = data.get("dob")

            # Validate the required fields
            if not all([full_name, contact_number, joining_date, gender, emergency_contact, dob]):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            # Validate the contact number (check if it's a valid format or length)
            if len(contact_number) < 10 or len(contact_number) > 15:
                return JsonResponse({"error": "Invalid contact number"}, status=400)

            # Validate the emergency contact number format as well
            if len(emergency_contact) < 10 or len(emergency_contact) > 15:
                return JsonResponse({"error": "Invalid emergency contact number"}, status=400)

            # Insert data into the Manager table along with the user_id
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO Manager (full_name, contact_number, joining_date, profile_image, gender, emergency_contact, dob, user_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, [full_name, contact_number, joining_date, profile_image, gender, emergency_contact, dob, user_id])

            return JsonResponse({"message": "Manager profile created successfully"}, status=201)

        except IntegrityError as e:
            return JsonResponse({"error": f"Integrity error: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def patch(self, request):
        try:
            if not request.user.is_authenticated:
                return JsonResponse({"error": "User not authenticated"}, status=401)

            user_id = request.user.id
            data = json.loads(request.body)

            # Build the update query dynamically based on provided fields
            update_fields = []
            values = []

            for field in ["full_name", "contact_number", "gender", "department", "position"]:
                if field in data:
                    update_fields.append(f"{field} = %s")
                    values.append(data[field])

            if not update_fields:
                return JsonResponse({"error": "No fields to update"}, status=400)

            # Add the user_id to values for the WHERE clause
            values.append(user_id)

            query = f"UPDATE Manager SET {', '.join(update_fields)} WHERE user_id = %s"

            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute(query, values)

            return JsonResponse({"message": "Manager profile updated successfully"}, status=200)

        except IntegrityError as e:
            return JsonResponse({"error": f"Integrity error: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def delete(self, request, manager_id):
        try:
            if not request.user.is_authenticated:
                return JsonResponse({"error": "User not authenticated"}, status=401)

            # Delete the manager record based on the provided manager_id
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM Manager WHERE manager_id = %s", [manager_id])
                    if cursor.rowcount == 0:
                        return JsonResponse({"error": "Manager not found"}, status=404)

            return JsonResponse({"message": "Manager profile deleted successfully"}, status=200)

        except IntegrityError as e:
            return JsonResponse({"error": f"Integrity error: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
