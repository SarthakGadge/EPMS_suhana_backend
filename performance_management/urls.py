from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .employee import EmployeeListView, PerformanceGoalCreateView, GetGoals
from .add_evaluation import PerformanceGoalDescriptionView, PerformanceEvaluationCreateView
from .views import (
    DepartmentViewSet,
    RoleViewSet,
    GoalViewSet,
    #     PerformanceEvaluationViewSet,
    #     PerformanceReviewViewSet,
    FeedbackViewSet,
    TrainingViewSet,
    EmployeeTrainingViewSet,
    NotificationViewSet,
    PerformanceEvaluationView,
    SelfEvaluationView
)

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'goals', GoalViewSet)
# router.register(r'evaluations', PerformanceEvaluationViewSet)
# router.register(r'reviews', PerformanceReviewViewSet)
router.register(r'feedback', FeedbackViewSet)
router.register(r'training', TrainingViewSet)
router.register(r'employee-training', EmployeeTrainingViewSet)
router.register(r'notifications', NotificationViewSet)
# router.register(r'employees', EmployeeListView, basename='employee')

urlpatterns = [
    path('', include(router.urls)),
    #     path('employees/', EmployeeListView.as_view(), name='employee-list'),
    path('setgoals/', PerformanceGoalCreateView.as_view(),
         name='create_performance_goal'),
    #     path('add_evaluation/', PerformanceGoalDescriptionView.as_view(),
    #          name='create_performance_goal'),
    #     path('submit_evaluation/', PerformanceEvaluationCreateView.as_view(),
    #          name='create_performance_goal'),
    #     path("performance_evaluation/",
    #          PerformanceEvaluationCreateView.as_view(), name='performance-eval'),
    path('evaluation/', SelfEvaluationView.as_view(),
         name='self-evaluation'),
    path('evaluation/<int:evaluation_id>/',
         SelfEvaluationView.as_view(), name='self-evaluation-update'),
    path("goals/", GetGoals.as_view(), name='get_goals')

]
