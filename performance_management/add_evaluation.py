# from rest_framework.views import APIView
# from django.db import connection, IntegrityError, transaction
# from django.http import JsonResponse
# from django.views import View
# from django.db import connection
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# import json


# @method_decorator(csrf_exempt, name='dispatch')
# class PerformanceGoalDescriptionView(View):
#     def post(self, request):
#         try:
#             # Parse JSON payload
#             data = json.loads(request.body)
#             employee_id = data.get("employee")

#             # Check if employee exists in the userauth_customuser table
#             with connection.cursor() as cursor:
#                 cursor.execute(
#                     "SELECT COUNT(*) FROM userauth_customuser WHERE id = %s", [employee_id])
#                 employee_exists = cursor.fetchone()[0]

#             if not employee_exists:
#                 return JsonResponse({"error": "Employee not found"}, status=404)

#             # Query to get all descriptions for the given employee_id
#             with connection.cursor() as cursor:
#                 cursor.execute("""
#                     SELECT description
#                     FROM performance_management_goal
#                     WHERE employee_id = %s
#                 """, [employee_id])
#                 descriptions = cursor.fetchall()

#             # Check if there are any descriptions
#             if not descriptions:
#                 return JsonResponse({"message": "No performance goals found for this employee"}, status=200)

#             # Format the descriptions into a list
#             descriptions_list = [desc[0] for desc in descriptions]

#             return JsonResponse({"descriptions": descriptions_list}, status=200)

#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)


# @method_decorator(csrf_exempt, name='dispatch')
# class PerformanceEvaluationCreateView(APIView):
#     def post(self, request):
#         try:
#             # Parse JSON payload
#             data = json.loads(request.body)
#             employee_id = data.get("employee_id")
#             goal_id = data.get("goal_id")
#             self_rating = data.get("self_rating")
#             manager_rating = data.get("manager_rating")
#             status = data.get("status")
#             # New field for manager feedback
#             manager_feedback = data.get("manager_feedback")

#             # Check if the goal and employee exist
#             with connection.cursor() as cursor:
#                 # Check for the employee
#                 cursor.execute(
#                     "SELECT COUNT(*) FROM userauth_customuser WHERE id = %s", [employee_id])
#                 employee_exists = cursor.fetchone()[0]

#                 # Retrieve description from the goal table if goal exists
#                 cursor.execute(
#                     "SELECT description FROM performance_management_goal WHERE id = %s", [goal_id])
#                 goal_data = cursor.fetchone()

#             if not employee_exists:
#                 return JsonResponse({"error": "Employee not found"}, status=404)
#             if not goal_data:
#                 return JsonResponse({"error": "Goal not found"}, status=404)

#             # Extract description from goal_data
#             description = goal_data[0]

#             # Calculate final_rating as the average of self_rating and manager_rating
#             if self_rating is not None and manager_rating is not None:
#                 final_rating = (self_rating + manager_rating) / 2
#             else:
#                 final_rating = None  # Handle case where ratings are missing

#             # Insert data into performance_management_performanceevaluation table
#             with transaction.atomic():
#                 with connection.cursor() as cursor:
#                     cursor.execute("""
#                         INSERT INTO performance_management_performanceevaluation
#                         (employee_id, goal_id, self_rating, manager_rating, final_rating, status, manager_feedback)
#                         VALUES (%s, %s, %s, %s, %s, %s, %s)
#                     """, [employee_id, goal_id, self_rating, manager_rating, final_rating, status, manager_feedback])

#             return JsonResponse({"message": "Performance evaluation created successfully"}, status=201)

#         except IntegrityError as e:
#             return JsonResponse({"error": f"Failed to create performance evaluation due to integrity error: {str(e)}"}, status=400)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)


# # from django.http import JsonResponse
# # from django.db import connection, IntegrityError, transaction
# # from rest_framework.views import APIView
# # from django.views.decorators.csrf import csrf_exempt
# # from django.utils.decorators import method_decorator
# # import json

# # @method_decorator(csrf_exempt, name='dispatch')
# # class PerformanceEvaluationCreateView(APIView):
# #     def post(self, request):
# #         try:
# #             # Parse JSON payload
# #             data = json.loads(request.body)
# #             employee_id = data.get("employee_id")
# #             goal_id = data.get("goal_id")
# #             manager_rating = data.get("manager_rating")
# #             status = data.get("status")
# #             manager_feedback = data.get("manager_feedback")  # New field for manager feedback

# #             # Check if the goal and employee exist
# #             with connection.cursor() as cursor:
# #                 # Check for the employee
# #                 cursor.execute("SELECT COUNT(*) FROM userauth_customuser WHERE id = %s", [employee_id])
# #                 employee_exists = cursor.fetchone()[0]

# #                 # Retrieve description and check if goal exists
# #                 cursor.execute("SELECT description FROM performance_management_goal WHERE id = %s", [goal_id])
# #                 goal_data = cursor.fetchone()

# #             if not employee_exists:
# #                 return JsonResponse({"error": "Employee not found"}, status=404)
# #             if not goal_data:
# #                 return JsonResponse({"error": "Goal not found"}, status=404)

# #             # Extract description from goal_data
# #             description = goal_data[0]

# #             # Retrieve self_rating from employee_rating table
# #             with connection.cursor() as cursor:
# #                 cursor.execute("SELECT self_rating FROM employee_rating WHERE employee_id = %s AND goal_id = %s", [employee_id, goal_id])
# #                 self_rating_data = cursor.fetchone()

# #             if not self_rating_data:
# #                 return JsonResponse({"error": "Self rating not found for this employee and goal"}, status=404)

# #             self_rating = self_rating_data[0]

# #             # Calculate final_rating as the average of self_rating and manager_rating
# #             final_rating = (self_rating + manager_rating) / 2 if manager_rating is not None else None

# #             # Insert data into performance_management_performanceevaluation table
# #             with transaction.atomic():
# #                 with connection.cursor() as cursor:
# #                     cursor.execute("""
# #                         INSERT INTO performance_management_performanceevaluation
# #                         (employee_id, goal_id, self_rating, manager_rating, final_rating, status, manager_feedback)
# #                         VALUES (%s, %s, %s, %s, %s, %s, %s)
# #                     """, [employee_id, goal_id, self_rating, manager_rating, final_rating, status, manager_feedback])

# #             return JsonResponse({"message": "Performance evaluation created successfully"}, status=201)

# #         except IntegrityError as e:
# #             return JsonResponse({"error": f"Failed to create performance evaluation due to integrity error: {str(e)}"}, status=400)
# #         except Exception as e:
# #             return JsonResponse({"error": str(e)}, status=500)


from rest_framework.views import APIView
from django.db import connection, IntegrityError, transaction
from django.http import JsonResponse
from django.views import View
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json


@method_decorator(csrf_exempt, name='dispatch')
class PerformanceGoalDescriptionView(View):
    def post(self, request):
        try:
            # Parse JSON payload
            data = json.loads(request.body)
            employee_id = data.get("employee_id")

            # Check if employee exists in the userauth_customuser table
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT COUNT(*) FROM employee WHERE employee_id = %s", [employee_id])
                employee_exists = cursor.fetchone()[0]

            if not employee_exists:
                return JsonResponse({"error": "Employee not found"}, status=404)

            # Query to get all descriptions for the given employee_id
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT description 
                    FROM performance_management_goal 
                    WHERE employee_id = %s
                """, [employee_id])
                descriptions = cursor.fetchall()

            # Check if there are any descriptions
            if not descriptions:
                return JsonResponse({"message": "No performance goals found for this employee"}, status=200)

            # Format the descriptions into a list
            descriptions_list = [desc[0] for desc in descriptions]

            return JsonResponse({"descriptions": descriptions_list}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class PerformanceEvaluationCreateView(APIView):
    def post(self, request):
        try:
            # Parse JSON payload
            data = json.loads(request.body)
            employee_id = data.get("employee_id")
            goal_id = data.get("goal_id")
            self_rating = data.get("self_rating")
            manager_rating = data.get("manager_rating")
            status = data.get("status")
            # New field for manager feedback
            manager_feedback = data.get("manager_feedback")

            # Check if the goal and employee exist
            with connection.cursor() as cursor:
                # Check for the employee
                cursor.execute(
                    "SELECT COUNT(*) FROM employee WHERE employee_id = %s", [employee_id])
                employee_exists = cursor.fetchone()[0]

                # Retrieve description from the goal table if goal exists
                cursor.execute(
                    "SELECT description FROM performance_management_goal WHERE id = %s", [goal_id])
                goal_data = cursor.fetchone()

            if not employee_exists:
                return JsonResponse({"error": "Employee not found"}, status=404)
            if not goal_data:
                return JsonResponse({"error": "Goal not found"}, status=404)

            # Extract description from goal_data
            description = goal_data[0]

            # Calculate final_rating as the average of self_rating and manager_rating
            if self_rating is not None and manager_rating is not None:
                final_rating = (self_rating + manager_rating) / 2
            else:
                final_rating = None  # Handle case where ratings are missing

            # Insert data into performance_management_performanceevaluation table
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO performance_management_performanceevaluation 
                        (employee_id, goal_id, self_rating, manager_rating, final_rating, status, manager_feedback)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, [employee_id, goal_id, self_rating, manager_rating, final_rating, status, manager_feedback])

            return JsonResponse({"message": "Performance evaluation created successfully"}, status=201)

        except IntegrityError as e:
            return JsonResponse({"error": f"Failed to create performance evaluation due to integrity error: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


# from django.http import JsonResponse
# from django.db import connection, IntegrityError, transaction
# from rest_framework.views import APIView
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# import json

# @method_decorator(csrf_exempt, name='dispatch')
# class PerformanceEvaluationCreateView(APIView):
#     def post(self, request):
#         try:
#             # Parse JSON payload
#             data = json.loads(request.body)
#             employee_id = data.get("employee_id")
#             goal_id = data.get("goal_id")
#             manager_rating = data.get("manager_rating")
#             status = data.get("status")
#             manager_feedback = data.get("manager_feedback")  # New field for manager feedback

#             # Check if the goal and employee exist
#             with connection.cursor() as cursor:
#                 # Check for the employee
#                 cursor.execute("SELECT COUNT(*) FROM userauth_customuser WHERE id = %s", [employee_id])
#                 employee_exists = cursor.fetchone()[0]

#                 # Retrieve description and check if goal exists
#                 cursor.execute("SELECT description FROM performance_management_goal WHERE id = %s", [goal_id])
#                 goal_data = cursor.fetchone()

#             if not employee_exists:
#                 return JsonResponse({"error": "Employee not found"}, status=404)
#             if not goal_data:
#                 return JsonResponse({"error": "Goal not found"}, status=404)

#             # Extract description from goal_data
#             description = goal_data[0]

#             # Retrieve self_rating from employee_rating table
#             with connection.cursor() as cursor:
#                 cursor.execute("SELECT self_rating FROM employee_rating WHERE employee_id = %s AND goal_id = %s", [employee_id, goal_id])
#                 self_rating_data = cursor.fetchone()

#             if not self_rating_data:
#                 return JsonResponse({"error": "Self rating not found for this employee and goal"}, status=404)

#             self_rating = self_rating_data[0]

#             # Calculate final_rating as the average of self_rating and manager_rating
#             final_rating = (self_rating + manager_rating) / 2 if manager_rating is not None else None

#             # Insert data into performance_management_performanceevaluation table
#             with transaction.atomic():
#                 with connection.cursor() as cursor:
#                     cursor.execute("""
#                         INSERT INTO performance_management_performanceevaluation
#                         (employee_id, goal_id, self_rating, manager_rating, final_rating, status, manager_feedback)
#                         VALUES (%s, %s, %s, %s, %s, %s, %s)
#                     """, [employee_id, goal_id, self_rating, manager_rating, final_rating, status, manager_feedback])

#             return JsonResponse({"message": "Performance evaluation created successfully"}, status=201)

#         except IntegrityError as e:
#             return JsonResponse({"error": f"Failed to create performance evaluation due to integrity error: {str(e)}"}, status=400)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)
