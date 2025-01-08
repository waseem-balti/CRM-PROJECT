from django.forms import PasswordInput
from django import forms
from rest_framework import serializers
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from crmapp.models import CustomUser
from datetime import datetime
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

CustomUser = get_user_model()

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)
    
    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("The new passwords do not match.")
        return data
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct.")
        return value
    
    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return value


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    uid = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        uid = force_str(urlsafe_base64_decode(data.get('uid')))
        try:
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            raise serializers.ValidationError("Invalid UID")

        token = data.get('token')
        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError("Invalid token")
        
        if data.get('new_password') != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords do not match")

        return data

    def save(self):
        uid = self.validated_data['uid']
        user = CustomUser.objects.get(pk=uid)
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'date_joined']


class RegisterCustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password], 
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
        style={'input_type': 'password'}
    )

    class Meta:
        model = CustomUser
        fields = (
            'email', 'first_name', 'last_name', 'password', 'password2',
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        # Check if email already exists
        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email is already registered."})

        return attrs

    def create(self, validated_data):
        # Create user with validated data
        user = CustomUser(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
    
        


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta :
        model = CustomUser
        fields = ['email','password'] 

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError(
                    {"detail": _("Invalid email or password.")},
                    code="authorization"
                )
            if not user.is_active:
                raise serializers.ValidationError(
                    {"detail": _("User account is disabled.")},
                    code="authorization"
                )

        else:
            raise serializers.ValidationError(
                {"detail": _("Must include 'email' and 'password'.")},
                code="authorization"
            )

        data['user'] = user
        return data