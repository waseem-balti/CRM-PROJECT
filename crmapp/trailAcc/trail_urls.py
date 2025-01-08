from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .trail_views import CustomUserViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='customuser')

urlpatterns = [
    path('api/', include(router.urls)),
]
