import os
import json
from django.conf import settings
from django.core.management import call_command
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

# Ensure you have a backups directory set up in your settings
BACKUPS_DIR = os.path.join(settings.BASE_DIR, 'backups')

if not os.path.exists(BACKUPS_DIR):
    os.makedirs(BACKUPS_DIR)

class DatabaseBackupView(APIView):
    def post(self, request, *args, **kwargs):
        """
        Handle backup creation via the API.
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"backup_{timestamp}.json"
            backup_filepath = os.path.join(settings.BASE_DIR, 'backups', backup_filename)
            
            with open(backup_filepath, 'w') as f:
                # Remove exclude parameter to include all models
                call_command('dumpdata', stdout=f)
            
            return Response({"message": f"Backup created successfully: {backup_filename}"}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DatabaseRestoreView(APIView):
    def post(self, request, *args, **kwargs):
        """
        Handle database restore via the API.
        """
        backup_file = request.data.get('backup_file', None)
        
        if not backup_file:
            return Response({"error": "Backup file is required."}, status=status.HTTP_400_BAD_REQUEST)

        backup_filepath = os.path.join(settings.BASE_DIR, 'backups', backup_file)
        
        if not os.path.exists(backup_filepath):
            return Response({"error": f"Backup file {backup_file} does not exist."}, status=status.HTTP_404_NOT_FOUND)

        try:
            with open(backup_filepath, 'r') as f:
                call_command('loaddata', f.name)
            return Response({"message": f"Database restored successfully from {backup_file}"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
