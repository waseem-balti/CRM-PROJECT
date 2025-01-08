from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from crmapp.models import ContactActivity
from .contact_activity_serializer import ContactActivitySerializer

class ContactActivityViewSet(viewsets.ModelViewSet):
    queryset = ContactActivity.objects.all()
    serializer_class = ContactActivitySerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except ContactActivity.DoesNotExist:
            raise NotFound("The requested ContactActivity does not exist.")

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": f"Failed to delete ContactActivity: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
