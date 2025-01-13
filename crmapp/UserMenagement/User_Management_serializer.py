from rest_framework import serializers
from crmapp.models import CustomUser


class UserManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name','phone_no','branch','department']




