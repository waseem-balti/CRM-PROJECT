from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from crmapp.models import Price
from .Price_serializer import PriceSerializer
from django.core.exceptions import ValidationError

class PriceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Price data.
    """
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PriceSerializer

    def get_queryset(self):
        return Price.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Price.DoesNotExist:
            return Response({'error': 'Price not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Failed to retrieve Price: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Price.DoesNotExist:
            return Response({'error': 'Price not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Failed to delete Price: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        """
        Validate and create a new Price instance.
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Failed to create Price: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        """
        Validate and update an existing Price instance.
        """
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Price.DoesNotExist:
            return Response({'error': 'Price not found'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Failed to update Price: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': f'Failed to retrieve Price: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, *args, **kwargs):
        """
        Handle partial updates to a Price instance.
        """
        try:
            return self.update(request, *args, partial=True, **kwargs)
        except Exception as e:
            return Response({'error': f'Failed to partially update Price: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_create(self, serializer):
        """
        Save the validated Price data during creation.
        """
        serializer.save()

    def perform_update(self, serializer):
        """
        Save the validated Price data during update.
        """
        serializer.save()

    def perform_destroy(self, instance):
        """
        Delete a Price instance.
        """
        instance.delete()
    
    def validate_price_data(self, data):
        """
        Add custom validation for Price data.
        """
        if data.get('price', 0) <= 0:
            raise ValidationError("Price value must be greater than zero.")
