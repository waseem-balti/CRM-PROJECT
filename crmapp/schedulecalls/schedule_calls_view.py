from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from crmapp.models import ScheduleCalls
from .schedule_calls_serializer import ScheduleCallsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

class ScheduleCallsViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
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
