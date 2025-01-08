from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from crmapp.models import Payment
from .payment_serializers import PaymentSerializer
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

class PaymentViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    
    def create(self, request, *args, **kwargs):
        """Handle creating a payment and processing it (simulating payment handling)"""
        try:
            with transaction.atomic():  # Ensure that the payment is only processed if everything is valid
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    payment = serializer.save()

                    # Simulate payment processing (here we can integrate an actual payment gateway)
                    if payment.amount < 100:
                        # Simulating a failed payment if the amount is below 100
                        payment.status = 'FAILED'
                        payment.save()
                        return Response({
                            "message": "Payment failed. Amount is too low."
                        }, status=status.HTTP_400_BAD_REQUEST)

                    # Simulating a successful payment
                    payment.status = 'COMPLETED'
                    payment.save()

                    return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Custom exception handling
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        """Handle updating a payment status"""
        payment = self.get_object()
        status = request.data.get('status')

        if status not in dict(Payment.STATUS_CHOICES):
            raise ValidationError("Invalid status update.")
        
        payment.status = status
        payment.save()

        return Response({
            "transaction_id": payment.transaction_id,
            "status": payment.status
        })
    
    def retrieve(self, request, *args, **kwargs):
        """Handle retrieving a payment"""
        try:
            payment = self.get_object()
            return Response(PaymentSerializer(payment).data)
        except Payment.DoesNotExist:
            raise NotFound("Payment not found.")

    def list(self, request, *args, **kwargs):
        """Handle listing payments with error handling for empty lists"""
        payments = self.get_queryset()

        if not payments:
            return Response({"message": "No payments found."}, status=status.HTTP_404_NOT_FOUND)

        return super().list(request, *args, **kwargs)
