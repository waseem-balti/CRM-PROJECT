from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response
from crmapp.models import UserProfile
from .user_profile_serializer import UserProfileSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing User Profiles based on the provided UserProfile model.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return a queryset filtered by the authenticated user.
        If the user is not authenticated, return an empty queryset.
        """
        user = self.request.user
        if not user.is_authenticated:
            return self.queryset.none()  # Return an empty queryset for unauthenticated users
        return self.queryset.filter(user=user)

    def perform_create(self, serializer):
        """
        Automatically set the user field when creating a new user profile.
        If the user is not authenticated, raise a permission denied exception.
        """
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to create a profile.")
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """
        Handle retrieval of a single user profile with error handling.
        """
        try:
            return super().retrieve(request, *args, **kwargs)
        except UserProfile.DoesNotExist:
            raise NotFound("The requested UserProfile does not exist.")
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, *args, **kwargs):
        """
        Handle deletion of a user profile with error handling.
        """
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": f"Failed to delete UserProfile: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
