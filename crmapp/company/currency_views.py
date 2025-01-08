from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from crmapp.models import Currency
from .currency_serializers import CurrencySerializer

class CurrencyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Currency data.
    """
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Handle retrieval of a single currency with error handling.
        """
        try:
            return super().retrieve(request, *args, **kwargs)
        except Currency.DoesNotExist:
            raise NotFound("The requested Currency does not exist.")
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        """
        Handle deletion of a currency with error handling.
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": f"Failed to delete Currency: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
