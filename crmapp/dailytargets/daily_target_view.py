from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from crmapp.models import DailyTarget
from .daily_target_serializer import DailyTargetSerializer

class DailyTargetViewSet(viewsets.ModelViewSet):
    queryset = DailyTarget.objects.all()
    serializer_class = DailyTargetSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except DailyTarget.DoesNotExist:
            raise NotFound("The requested DailyTarget does not exist.")

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": f"Failed to delete DailyTarget: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
