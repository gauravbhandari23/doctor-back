from rest_framework import serializers
from datetime import datetime
from .models import PatientProfile

class PatientProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    phone = serializers.CharField(source='user.phone', read_only=True)
    date_of_birth = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'])

    class Meta:
        model = PatientProfile
        fields = ['id', 'email', 'username', 'phone', 'medical_history', 'date_of_birth', 'gender', 'address', 'blood_type', 'allergies', 'current_medications', 'chronic_conditions', 'insurance_provider']
