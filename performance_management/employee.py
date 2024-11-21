import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import connection, IntegrityError, transaction
from django.views import View
from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Goal
from .serializers import GoalSerializer
from rest_framework import status


class GetGoals(APIView):
    def get(self, request):
        try:
            goals = Goal.objects.all()
            serializer = GoalSerializer(goals, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmployeeListView(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            # Query to select employee_id, first_name, and last_name from userauth_customuser where role is 'employee'
            cursor.execute(
                "SELECT id, first_name, last_name FROM userauth_customuser WHERE role = %s", ["employee"])
            rows = cursor.fetchall()

        # Formatting the response to include 'employee_name_id' with concatenated name and ID
        employees = [
            {
                # Check if both first_name and last_name are present
                # Concatenate name if present, else just show employee_id
                'employee_name_id': f"{row[1]} {row[2]} {row[0]}" if row[1] and row[2] else f"{row[0]}"
            }
            for row in rows
        ]

        return JsonResponse({'employees': employees})


@method_decorator(csrf_exempt, name='dispatch')
class PerformanceGoalCreateView(View):
    def post(self, request):
        try:
            # Parse JSON payload
            data = json.loads(request.body)
            employee_id = data.get("employee_id")
            description = data.get("description")
            weightage = data.get("weightage")
            start_date = data.get("start_date")
            end_date = data.get("end_date")
            status = data.get("status")

            # Check if employee exists in the userauth_customuser table
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM employee WHERE employee_id = %s", [employee_id])
                employee_exists = cursor.fetchone()[0]

            if not employee_exists:
                return JsonResponse({"error": "Employee not found"}, status=404)

            # Insert data into performance_management_goal table
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO performance_management_goal (employee_id, description, weightage, start_date, end_date, status)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, [employee_id, description, weightage, start_date, end_date, status])

            return JsonResponse({"message": "Performance goal created successfully"}, status=201)

        except IntegrityError as e:
            return JsonResponse({"error": f"Failed to create performance goal due to integrity error: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class PerformanceGoalUpdateView(View):
    def patch(self, request, employee_id, goal_id):
        try:
            # Parse JSON payload
            data = json.loads(request.body)
            description = data.get("description")
            weightage = data.get("weightage")
            start_date = data.get("start_date")
            end_date = data.get("end_date")
            status = data.get("status")

            # Ensure at least one field is provided for update
            if not any([description, weightage, start_date, end_date, status]):
                return JsonResponse({"error": "No fields provided to update"}, status=400)

            # Build dynamic query for updating fields
            update_fields = []
            params = []

            if description is not None:
                update_fields.append("description = %s")
                params.append(description)
            if weightage is not None:
                update_fields.append("weightage = %s")
                params.append(weightage)
            if start_date is not None:
                update_fields.append("start_date = %s")
                params.append(start_date)
            if end_date is not None:
                update_fields.append("end_date = %s")
                params.append(end_date)
            if status is not None:
                update_fields.append("status = %s")
                params.append(status)

            params.extend([goal_id, employee_id])

            # Check if the specific goal exists for the given employee_id
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM performance_management_goal
                    WHERE id = %s AND employee_id = %s
                """, [goal_id, employee_id])
                if cursor.fetchone()[0] == 0:
                    return JsonResponse({"error": "Goal not found for the given employee"}, status=404)

            # Update the record in the database
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute(f"""
                        UPDATE performance_management_goal
                        SET {', '.join(update_fields)}
                        WHERE id = %s AND employee_id = %s
                    """, params)

            return JsonResponse({"message": "Performance goal updated successfully"}, status=200)

        except IntegrityError as e:
            return JsonResponse({"error": f"Failed to update performance goal due to integrity error: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


# import json
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
# from django.db import connection, IntegrityError, transaction
# from django.views import View
# from django.http import JsonResponse
# from django.db import connection
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import Goal
# from .serializers import GoalSerializer
# from rest_framework import status


# class EmployeeListView(APIView):
#     def get(self, request):
#         with connection.cursor() as cursor:
#             # Query to select employee_id, first_name, and last_name from userauth_customuser where role is 'employee'
#             cursor.execute(
#                 "SELECT id, first_name, last_name FROM userauth_customuser WHERE role = %s", ["employee"])
#             rows = cursor.fetchall()

#         # Formatting the response to include 'employee_name_id' with concatenated name and ID
#         employees = [
#             {
#                 # Check if both first_name and last_name are present
#                 # Concatenate name if present, else just show employee_id
#                 'employee_name_id': f"{row[1]} {row[2]} {row[0]}" if row[1] and row[2] else f"{row[0]}"
#             }
#             for row in rows
#         ]

#         return JsonResponse({'employees': employees})


# @method_decorator(csrf_exempt, name='dispatch')
# class PerformanceGoalCreateView(View):
#     def post(self, request):
#         try:
#             # Parse JSON payload
#             data = json.loads(request.body)
#             employee_id = data.get("employee")
#             description = data.get("description")
#             weightage = data.get("weightage")
#             start_date = data.get("start_date")
#             end_date = data.get("end_date")
#             status = data.get("status")

#             # Check if employee exists in the userauth_customuser table
#             with connection.cursor() as cursor:
#                 cursor.execute(
#                     "SELECT COUNT(*) FROM userauth_customuser WHERE id = %s", [employee_id])
#                 employee_exists = cursor.fetchone()[0]

#             if not employee_exists:
#                 return JsonResponse({"error": "Employee not found"}, status=404)

#             # Insert data into performance_management_goal table
#             with transaction.atomic():
#                 with connection.cursor() as cursor:
#                     cursor.execute("""
#                         INSERT INTO performance_management_goal (employee_id, description, weightage, start_date, end_date, status)
#                         VALUES (%s, %s, %s, %s, %s, %s)
#                     """, [employee_id, description, weightage, start_date, end_date, status])

#             return JsonResponse({"message": "Performance goal created successfully"}, status=201)

#         except IntegrityError as e:
#             return JsonResponse({"error": f"Failed to create performance goal due to integrity error: {str(e)}"}, status=400)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)
