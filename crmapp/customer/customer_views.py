from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from crmapp.models import CustomUser
from .customer_serializer import CustomerSerializer
from crmapp.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomerViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializer
    renderer_classes = [UserRenderer]

    def get_queryset(self):
        return CustomUser.objects.all()
    

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except CustomUser.DoesNotExist:
            raise NotFound("The requested Customer does not exist.")

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": f"Failed to delete Customer: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
           )