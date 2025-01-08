from rest_framework import viewsets, status
from crmapp.models import Lead
from .lead_Serializers import LeadSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

class LeadViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Lead.objects.all()  # Retrieve all Lead objects
    serializer_class = LeadSerializer  # Use the LeadSerializer

    # Optionally, you can add filtering, search, or custom behavior
    ordering_fields = ['date_created']
    ordering = ['-date_created']

    def retrieve(self, request, *args, **kwargs):
        """
        Handle retrieval of a single lead with error handling.
        """
        try:
            return super().retrieve(request, *args, **kwargs)
        except Lead.DoesNotExist:
            raise NotFound("The requested Lead does not exist.")
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        """
        Handle deletion of a lead with error handling.
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": f"Failed to delete Lead: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
