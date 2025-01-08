# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .payment_views import PaymentViewSet

router = DefaultRouter()
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('payment/', include(router.urls)),
]
