from django.urls import include, path
from rest_framework import routers
from .schedule_calls_view import ScheduleCallsViewSet

router = routers.DefaultRouter()
router.register(r'schedule-calls', ScheduleCallsViewSet, basename='schedule-calls')

urlpatterns = [
    path('api/', include(router.urls)),
]
