from rest_framework import serializers
from crmapp.models import Branch

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['company','name','location','contact_person','contact_email','contact_phone'] 
        read_only_fields = ['created_by']

