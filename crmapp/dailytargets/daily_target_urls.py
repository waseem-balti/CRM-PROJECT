from django.urls import include, path
from rest_framework import routers
from .daily_target_view import DailyTargetViewSet

router = routers.DefaultRouter()
router.register(r'daily-targets', DailyTargetViewSet, basename='daily-targets')

urlpatterns = [
    path('api/', include(router.urls)),
]
