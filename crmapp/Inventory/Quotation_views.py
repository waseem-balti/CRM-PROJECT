from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from crmapp.models import ProductQuotation
from .Quotation_serializer import ProductQuotationSerializer

class ProductQuotationViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProductQuotationSerializer

    def get_queryset(self):
        """
        Returns all ProductQuotations for the current user or branch.
        You can modify this to filter based on user, branch, or other fields if needed.
        """
        return ProductQuotation.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Handle the creation of a new ProductQuotation.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Auto-calculate total_price if not provided
            if 'total_price' not in serializer.validated_data or serializer.validated_data['total_price'] is None:
                quantity = serializer.validated_data['quantity']
                unit_price = serializer.validated_data['unit_price']
                total_price = quantity * unit_price
                serializer.validated_data['total_price'] = total_price

            # Save the new ProductQuotation
            serializer.save()

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def update(self, request, *args, **kwargs):
        """
        Handle updating an existing ProductQuotation.
        """
        instance = self.get_object()  # Get the existing ProductQuotation instance
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            # Auto-calculate total_price if not provided
            if 'total_price' not in serializer.validated_data or serializer.validated_data['total_price'] is None:
                quantity = serializer.validated_data['quantity']
                unit_price = serializer.validated_data['unit_price']
                total_price = quantity * unit_price
                serializer.validated_data['total_price'] = total_price

            # Save the updated ProductQuotation
            serializer.save()

            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def destroy(self, request, *args, **kwargs):
        """
        Handle deleting a ProductQuotation.
        """
        try:
            instance = self.get_object()
            instance.delete()  # Delete the ProductQuotation
            return Response({"message": "ProductQuotation deleted successfully."}, status=204)
        except ProductQuotation.DoesNotExist:
            raise NotFound("ProductQuotation not found")
        except Exception as e:
            return Response({'error': f'Failed to delete ProductQuotation: {str(e)}'}, status=500)

    def retrieve(self, request, *args, **kwargs):
        """
        Handle retrieving a specific ProductQuotation by its ID.
        """
        try:
            return super().retrieve(request, *args, **kwargs)
        except ProductQuotation.DoesNotExist:
            raise NotFound('ProductQuotation not found')
        except Exception as e:
            return Response({'error': f'Failed to retrieve ProductQuotation: {str(e)}'}, status=500)
