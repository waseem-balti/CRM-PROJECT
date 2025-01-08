from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .user_profile_views import UserProfileViewSet

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='user-profile')

urlpatterns = [
    path('users/', include(router.urls)),
]
