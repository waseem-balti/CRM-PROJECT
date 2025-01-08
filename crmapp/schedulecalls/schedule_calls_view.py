from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from crmapp.models import ScheduleCalls
from .schedule_calls_serializer import ScheduleCallsSerializer

class ScheduleCallsViewSet(viewsets.ModelViewSet):
    queryset = ScheduleCalls.objects.all()
    serializer_class = ScheduleCallsSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except ScheduleCalls.DoesNotExist:
            raise NotFound("The requested ScheduleCall does not exist.")

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": f"Failed to delete ScheduleCall: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
