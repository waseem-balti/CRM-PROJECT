from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from crmapp.models import Lead
from .customer_serializer import CustomerSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Customer data.
    """
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializer

    def get_queryset(self):
        """
        Return a queryset of leads marked as customers.
        """
        return Lead.objects.filter(is_customer=True)

    def retrieve(self, request, *args, **kwargs):
        """
        Handle retrieval of a single customer with error handling.
        """
        try:
            return super().retrieve(request, *args, **kwargs)
        except Lead.DoesNotExist:
            raise NotFound("The requested Customer does not exist.")
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        """
        Handle deletion of a customer with error handling.
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": f"Failed to delete Customer: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
