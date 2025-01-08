from rest_framework import serializers
from crmapp.models import Department , DpartmentalGoal

class CompanyDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['branch', 'name', 'description','created_by']


class CompanyDpartmentalGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = DpartmentalGoal
        fields = ['department', 'mission', 'from_date','created_by','to_date','goal']
