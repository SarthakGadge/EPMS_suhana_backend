from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FeedbackCreateView, FeedbackViewSet, ManagerListView

router = DefaultRouter()
router.register(r'feedback', FeedbackViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(router.urls)),
    path('employeetomanager_feedback/', FeedbackCreateView.as_view(),
         name='create_performance_goal'),
    path('list_managers/', ManagerListView.as_view(), name='list_managers'),

]
