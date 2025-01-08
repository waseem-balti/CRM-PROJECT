from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from crmapp.models import Organization
from .Orgnaization_Serializer import OrganizationSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        return Organization.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Organization.DoesNotExist:
            raise NotFound('Organization not found')
        except Exception as e:
            return Response({'error': f'Failed to retrieve Organization: {str(e)}'}, status=500)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)  # For PATCH requests
            instance = self.get_object()
            serializer = self.serializer_class(instance, data=request.data, partial=partial)
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise ValidationError(serializer.errors)
        except Organization.DoesNotExist:
            raise NotFound('Organization not found')
        except ValidationError as e:
            return Response({'validation_errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Failed to update Organization: {str(e)}'}, status=500)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'message': 'Organization deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Organization.DoesNotExist:
            raise NotFound('Organization not found')
        except Exception as e:
            return Response({'error': f'Failed to delete Organization: {str(e)}'}, status=500)
