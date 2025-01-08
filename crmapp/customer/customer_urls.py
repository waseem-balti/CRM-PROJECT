from django.urls import include, path
from rest_framework import routers
from .customer_views import CustomerViewSet

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customers')

urlpatterns = [
    path('api/', include(router.urls)),
]
