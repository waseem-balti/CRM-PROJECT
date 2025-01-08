from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from crmapp.models import KPI
from .kpi_serializers import KPISerializer

class KPIViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = KPISerializer

    def get_queryset(self):
        """
        Return all KPIs, apply filtering logic if needed in the future.
        """
        queryset = KPI.objects.all()
        return queryset

    def retrieve(self, request, *args, **kwargs):
        """
        Handle retrieval of a single KPI with error handling.
        """
        try:
            return super().retrieve(request, *args, **kwargs)
        except KPI.DoesNotExist:
            raise NotFound("The requested KPI does not exist.")
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        """
        Handle deletion of a KPI with error handling.
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": f"Failed to delete KPI: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
