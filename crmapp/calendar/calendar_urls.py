from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .calendar_views import EventViewSet, CategoryViewSet, CalendarViewSet

# Initialize the router
router = DefaultRouter()

# Register ViewSets
router.register(r'events', EventViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'calendar', CalendarViewSet, basename='calendar')  # Explicitly specify basename

# Define URL patterns
urlpatterns = [
    # Include router-generated URLs
    path('calendar/', include(router.urls)),
    path('calendar/events-by-date/', CalendarViewSet.as_view({'get': 'events_by_date'}), name='calendar-events-by-date'),
]
