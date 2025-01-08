from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from crmapp.models import Lead
from .opportunity_serializer import OpportunitySerializer

class OpportunityViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OpportunitySerializer

    def get_queryset(self):
        """
        Return a queryset of leads marked as opportunities and not customers.
        """
        return Lead.objects.filter(move_to_opportunity=True, is_customer=False)

    def retrieve(self, request, *args, **kwargs):
        """
        Handle retrieval of a single opportunity with error handling.
        """
        try:
            return super().retrieve(request, *args, **kwargs)
        except Lead.DoesNotExist:
            raise NotFound("The requested Opportunity does not exist.")
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        """
        Handle deletion of an opportunity with error handling.
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": f"Failed to delete Opportunity: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
