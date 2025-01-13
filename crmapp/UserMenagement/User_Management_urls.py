from django.urls import path,include
from rest_framework import routers
from .User_Management_views import UserManagementViewSet

router = routers.DefaultRouter()
router.register('UserManagement', UserManagementViewSet ,basename='UserManagement')

urlpatterns = [
    path('api/', include(router.urls)),
]
