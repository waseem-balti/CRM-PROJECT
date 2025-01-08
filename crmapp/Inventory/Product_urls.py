from django.urls import path ,include
from rest_framework import routers
from .Product_views import ProductViewset, ProductServiceViewset

router = routers.DefaultRouter()
router.register(r'products', ProductViewset, basename='products')
router.register(r'product-services', ProductServiceViewset, basename='product-services')

urlpatterns = [
    path('api/', include(router.urls)),
]