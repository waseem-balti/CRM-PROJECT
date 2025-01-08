from django.urls import include, path, re_path
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from crmapp.Auth.auth_views import (
    ChangePasswordView,
    ForgotPasswordView,
    LogoutView,
    ResetPasswordView,
    RegisterCustomUserViewSet
)


router = routers.DefaultRouter()
router.register(r"register", RegisterCustomUserViewSet, basename="register")


urlpatterns = [
    # Below are for auth
    path("logout", LogoutView.as_view(), name="logout"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
    # re_path(r"^docs/(?P<path>.*)$", TemplateView.as_view(template_name="docs.html")),
    path("", include(router.urls)),
]