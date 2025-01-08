from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from crmapp.models import CustomUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth import get_user_model, authenticate
from .auth_serializers import ChangePasswordSerializer,   ForgotPasswordSerializer, RegisterCustomUserSerializer,  LoginSerializer, ResetPasswordSerializer
from rest_framework_simplejwt.exceptions import InvalidToken


User = get_user_model()

class ChangePasswordView(APIView):
    """
    An endpoint for changing password.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    """
    View to handle forgot password requests.
    """
    serializer_class = ForgotPasswordSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"https://smms-app-ec48c9-7ad1bc-65-108-245-140.traefik.me/auth/forgot-password?uid={uid}&token={token}"
            
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                'no-reply@example.com',
                [email],
            )
            return Response({"message": "Password reset link sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    """
    View to handle password reset.
    """
    serializer_class = ResetPasswordSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterCustomUserViewSet(viewsets.ModelViewSet):
    serializer_class = RegisterCustomUserSerializer
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        all_users = CustomUser.objects.all()
        return all_users

    def perform_create(self, serializer):
        serializer.save()


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, JWTAuthentication]

def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                raise InvalidToken("Refresh token is required.")

            token = RefreshToken(refresh_token)
            token.blacklist()
            request.session.flush()

            return Response({"detail": "Logout successful."}, status=status.HTTP_200_OK)
        except InvalidToken as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)