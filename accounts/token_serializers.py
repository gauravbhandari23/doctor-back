from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['is_verified'] = user.is_verified
        token['user_type'] = user.user_type
        return token

    def validate(self, attrs):
        # Use email for authentication
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }
        User = get_user_model()
        user = User.objects.filter(email=credentials['email']).first()
        if user and user.check_password(credentials['password']):
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            data = super().validate(attrs)
            return data
        raise serializers.ValidationError('No active account found with the given credentials')