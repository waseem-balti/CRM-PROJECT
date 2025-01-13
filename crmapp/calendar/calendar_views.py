from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.decorators import action
from crmapp.models import Event, Category, Calendar
from .calendar_serializers import EventSerializer, CategorySerializer, CalendarSerializer

class EventViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CalendarViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Calendar.
    """
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CalendarSerializer

    def get_queryset(self):
        """
        Override to filter events based on the date.
        """
        queryset = Calendar.objects.all()
        date = self.request.query_params.get("date")
        if date:
            queryset = queryset.filter(date=date)
        return queryset

    def edit(self, request, pk=None):
        """
        Handle editing a calendar entry.
        """
        try:
            calendar = Calendar.objects.get(pk=pk)
        except Calendar.DoesNotExist:
            return Response({"error": "Calendar entry not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CalendarSerializer(calendar, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """
        Handle deletion of a calendar entry.
        """
        try:
            calendar = Calendar.objects.get(pk=pk)
        except Calendar.DoesNotExist:
            return Response({"error": "Calendar entry not found."}, status=status.HTTP_404_NOT_FOUND)

        calendar.delete()
        return Response({"message": "Calendar entry deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        """
        Handle retrieval of a calendar entry with events for a specific date.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Handle deletion of a calendar entry with error handling.
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": f"Failed to delete Calendar entry: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request, *args, **kwargs):
        """
        Handle creation of a calendar entry and associate events on the provided date.
        """
        date = request.data.get("date")
        event_ids = request.data.get('event_ids', [])
        if not date:
            return Response({"error": "Date is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure Calendar entry exists for the date
        calendar, created = Calendar.objects.get_or_create(date=date)
        # Add the events to the calendar date
        events = Event.objects.filter(id__in=event_ids)
        if not events.exists():
            return Response(
                {"error": "No valid events found for the provided IDs."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Return the updated calendar object
        serializer = self.get_serializer(calendar)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def events_by_date(self, request):
        """
        Custom action to retrieve events by date.
        """
        date = request.query_params.get('date')
        if not date:
            return Response({"error": "Date is required."}, status=status.HTTP_400_BAD_REQUEST)

        events = Event.objects.filter(date=date)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
