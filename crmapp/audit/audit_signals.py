from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from crmapp.models import AuditLog
from django.utils.timezone import now

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    AuditLog.objects.create(
        user=user,
        action="User Logged In",
        timestamp=now(),
        ip_address=request.META.get('REMOTE_ADDR'),
        description=f"User {user.email} logged in from IP {request.META.get('REMOTE_ADDR')}"
    )

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    AuditLog.objects.create(
        user=user,
        action="User Logged Out",
        timestamp=now(),
        ip_address=request.META.get('REMOTE_ADDR'),
        description=f"User {user.email} logged out"
    )

@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    AuditLog.objects.create(
        action="Failed Login Attempt",
        timestamp=now(),
        ip_address=request.META.get('REMOTE_ADDR'),
        description=f"Failed login attempt for user {credentials.get('username', '')} from IP {request.META.get('REMOTE_ADDR')}"
    )
