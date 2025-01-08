from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from crmapp.models import Invoice
from .invoice_serializer import InvoiceSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

class InvoiceViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific invoice with error handling."""
        try:
            return super().retrieve(request, *args, **kwargs)
        except Invoice.DoesNotExist:
            raise NotFound("The requested invoice does not exist.")

    def destroy(self, request, *args, **kwargs):
        """Handle deletion of an invoice."""
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": f"An error occurred while deleting the invoice: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
