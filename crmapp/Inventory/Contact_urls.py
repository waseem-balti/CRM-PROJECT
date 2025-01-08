from django.urls import include, path
from rest_framework import routers
from .Contact_views import ContactListView

router = routers.DefaultRouter()
router.register(r'Contact', ContactListView, basename='contact-summaries')

urlpatterns = [
    path('api/', include(router.urls)),
]
