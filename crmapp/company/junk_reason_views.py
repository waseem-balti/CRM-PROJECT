from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from crmapp.models import JunkReason
from .junk_reason_serializers import JunkReasonSerializer

class JunkReasonViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = JunkReasonSerializer

    def get_queryset(self):
        """
        Return queryset filtered by lead_id if provided.
        """
        lead_id = self.request.query_params.get('lead', None)
        queryset = JunkReason.objects.all()
        if lead_id:
            queryset = queryset.filter(lead_id=lead_id)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        """
        Handle retrieval of a single junk reason with error handling.
        """
        try:
            return super().retrieve(request, *args, **kwargs)
        except JunkReason.DoesNotExist:
            raise NotFound("The requested JunkReason does not exist.")
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        """
        Handle deletion of a junk reason with error handling.
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": f"Failed to delete JunkReason: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
