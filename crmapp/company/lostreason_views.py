from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from crmapp.models import LostReason
from .lostreason_serializers import LostReasonSerializer

class LostReasonViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = LostReasonSerializer

    def get_queryset(self):
        """
        Fetch lost reasons based on lead, or return all if no lead ID is provided.
        """
        lead_id = self.request.query_params.get('lead', None)
        queryset = LostReason.objects.all()
        if lead_id:
            queryset = queryset.filter(lead_id=lead_id)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        """
        Handle retrieval of a single lost reason with error handling.
        """
        try:
            return super().retrieve(request, *args, **kwargs)
        except LostReason.DoesNotExist:
            raise NotFound("The requested LostReason does not exist.")
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        """
        Handle deletion of a lost reason with error handling.
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": f"Failed to delete LostReason: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
