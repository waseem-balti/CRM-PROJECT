from django.urls import include, path, re_path
from rest_framework import routers
from django.views.generic import TemplateView
from .company_department_views import DepartmentViewSet, CompanyDpartmentalGoalViewSet

# Initialize the router
router = routers.DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='CompanyDepartments') 
router.register(r'dpartmental-goals', CompanyDpartmentalGoalViewSet, basename='CompanyDpartmentalGoals') 

urlpatterns = [
    # Documentation URL
    re_path(r'^docs/(?P<path>.*)$', TemplateView.as_view(template_name='docs.html')),

    # Include the router-generated URLs for the branches viewset
    path('api/', include(router.urls)),  # All API endpoints will be prefixed with 'api/'

]
