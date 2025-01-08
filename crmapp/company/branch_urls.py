from django.urls import include, path, re_path
from rest_framework import routers
from .branch_views import BranchViewSet
from django.views.generic import TemplateView

# Initialize the router
router = routers.DefaultRouter()
router.register(r'branches', BranchViewSet, basename='branches')  # Register the BranchViewSet

urlpatterns = [
    # Documentation URL

    path('branches/<int:pk>/edit/', BranchViewSet.as_view({'patch': 'edit'}), name='branch-edit'),
    path('branches/<int:pk>/delete/', BranchViewSet.as_view({'delete': 'delete'}), name='branch-delete'),
    # Include the router-generated URLs for the branches viewset
    path('api/', include(router.urls)),  # All API endpoints will be prefixed with 'api/'

]
