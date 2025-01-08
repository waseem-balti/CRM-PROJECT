from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from crmapp.models import CustomUser, TrialedEmail  
from .trail_serializers import CustomUserSerializer, TrialStatusSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.timezone import now

class CustomUserViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer

    # Filter queryset to include only users with active trials
    def get_queryset(self):
        return CustomUser.objects.filter(trial=True, trial_end_date__gt=now())


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
