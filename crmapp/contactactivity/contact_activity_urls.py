from django.urls import include, path
from rest_framework import routers
from .contact_activity_view import ContactActivityViewSet

router = routers.DefaultRouter()
router.register(r'contact-activities', ContactActivityViewSet, basename='contact-activities')

urlpatterns = [
    path('api/', include(router.urls)),
]
