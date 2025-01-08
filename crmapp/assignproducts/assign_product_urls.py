from django.urls import include, path
from rest_framework import routers
from .assign_product_view import AssignProductViewSet

router = routers.DefaultRouter()
router.register(r'assign-products', AssignProductViewSet, basename='assign-products')

urlpatterns = [
    path('api/', include(router.urls)),
]
