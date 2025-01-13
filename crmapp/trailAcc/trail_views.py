from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework import viewsets, status
from crmapp.models import CustomUser
from .trail_serializers import RegisterCustomUserSerializer
from rest_framework.decorators import action

class RegisterCustomUserViewSet(viewsets.ModelViewSet):
    serializer_class = RegisterCustomUserSerializer
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Notify trial expiration if applicable
        for user in CustomUser.objects.all():
            user.check_trial_status()
        return CustomUser.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            if user.is_trial_expired:
                return Response(
                    {"message": "Your trial has expired. Please upgrade your account."},
                    status=status.HTTP_403_FORBIDDEN
                )
        return super().list(request, *args, **kwargs)


    @action(detail=True, methods=['get'], url_path='trial-status')
    def trial_status(self, request, pk=None):
        """
        Check if the user's trial is active or expired, and handle expiration logic.
        """
        user = self.get_object()

        # Check if the user has already availed the trial
        if TrialedEmail.objects.filter(email=user.email).exists():
            return Response(
                {"message": "Trial already availed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update the trial status if expired
        if user.is_trial_expired():
            user.trial = False
            user.save()

            # Add email to TrialedEmail if not already present
            TrialedEmail.objects.get_or_create(email=user.email)

            # Do not return active trial data for expired trials
            return Response(
                {"message": "Trial period has expired."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # If the trial is still active
        serializer = TrialStatusSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)



    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def reactivate_trial(self, request, pk=None):
        user = self.get_object()
        try:
            user.reactivate_trial()
            return Response(
                {"message": "Trial reactivated successfully."},
                status=status.HTTP_200_OK
            )
        except ValueError as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
