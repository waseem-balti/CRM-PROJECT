from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from crmapp.models import AuditLog
from django.utils.timezone import now
from crmapp.renderers import UserRenderer

User = get_user_model()

class ChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        new_password = request.data.get('new_password')
        user.set_password(new_password)
        user.save()

        # Log the audit event
        AuditLog.objects.create(
            user=user,
            action="Password Change",
            timestamp=now(),
            ip_address=request.META.get('REMOTE_ADDR'),
            description=f"User {user.email} changed password"
        )
        
        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
