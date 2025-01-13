from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from crmapp.models import Contest
from .contest_serializers import ContestSerializer

class ContestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Contest data.
    """
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ContestSerializer

    def get_queryset(self):
        """
        Return contests assigned to the current user.
        """
        return Contest.objects.filter(assigned_to=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Customize the creation of a new contest.
        """
        data = request.data.copy()
        data['assigned_to'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
