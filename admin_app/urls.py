from django.urls import path
from .views import CreateUserView, AdminUpdateView

urlpatterns = [
    path('create_user/', CreateUserView.as_view(), name='create-user'),
    path('admin/update/', AdminUpdateView.as_view(), name='admin-update'),
]
