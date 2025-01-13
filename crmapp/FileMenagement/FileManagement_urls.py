from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .FileManagement_views import FileViewSet, FolderViewSet

router = DefaultRouter()
router.register(r'folders', FolderViewSet, basename='folder')
router.register(r'files', FileViewSet, basename='file')

urlpatterns = [
    path('', include(router.urls)),
]
