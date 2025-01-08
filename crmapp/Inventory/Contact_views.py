import logging
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from crmapp.models import Contact
from .Contact_serializer import ContactSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

# Set up logging
logger = logging.getLogger(__name__)
class ServerError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "A server error occurred. Please try again later."
    default_code = "server_error"

class ContactListView(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ContactSerializer

    def get_queryset(self):
        """
        Return a queryset of all contacts.
        """
        try:
            return Contact.objects.all()
        except Exception as e:
            logger.error(f"Error fetching contacts: {e}")
            raise ServerError("Unable to fetch contacts at the moment. Please try again later.")

    @action(detail=True, methods=['get'], url_path='get-contact-details')
    def get_contact_details(self, request, pk=None):
        """
        Retrieve contact details by ID.
        """
        try:
            contact = self.get_object()
            serializer = ContactSerializer(contact)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Contact.DoesNotExist:
            logger.error(f"Contact with ID {pk} not found.")
            return Response({"error": "Contact not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error retrieving contact details: {e}")
            raise ServerError()

    @action(detail=True, methods=['put'], url_path='update-contact')
    def update_contact(self, request, pk=None):
        """
        Update contact details by ID.
        """
        try:
            contact = self.get_object()
            serializer = ContactSerializer(contact, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Contact.DoesNotExist:
            logger.error(f"Contact with ID {pk} not found.")
            return Response({"error": "Contact not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error updating contact: {e}")
            raise ServerError()

    @action(detail=True, methods=['delete'], url_path='delete-contact')
    def delete_contact(self, request, pk=None):
        """
        Delete contact by ID.
        """
        try:
            contact = self.get_object()
            contact.delete()
            return Response({"message": "Contact deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Contact.DoesNotExist:
            logger.error(f"Contact with ID {pk} not found.")
            return Response({"error": "Contact not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting contact: {e}")
            raise ServerError()
