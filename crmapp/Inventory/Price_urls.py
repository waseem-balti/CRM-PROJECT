from django.urls import path,include
from rest_framework import routers
from .Price_views import PriceViewSet

router = routers.DefaultRouter()

router.register(r'Price', PriceViewSet, basename='price')

urlpatterns = [
    path('api/', include(router.urls)),
]