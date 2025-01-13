from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from crmapp.models import Upload_Project
from .Project_serializer import UploadProjectSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Project data.
    """
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UploadProjectSerializer

    def get_queryset(self):
        return Upload_Project.objects.all()
    
    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Upload_Project.DoesNotExist:
            raise NotFound("Project does not exist.")
    
    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": f"Failed to delete project: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


