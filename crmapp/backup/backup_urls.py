from django.urls import path
from .backup_restore_views import DatabaseBackupView, DatabaseRestoreView

urlpatterns = [
    path('backup/', DatabaseBackupView.as_view(), name='database-backup'),
    path('restore/', DatabaseRestoreView.as_view(), name='database-restore'),
]
