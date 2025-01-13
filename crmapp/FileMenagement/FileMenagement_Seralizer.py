from rest_framework import serializers
from  crmapp.models import File, Folder

class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['id', 'name', 'created_by', 'created_at']

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'name', 'folder', 'owner', 'size', 'uploaded_at', 'file_type', 'path']
