from rest_framework import serializers
from .models_rating import DoctorRating

class DoctorRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorRating
        fields = ['id', 'doctor', 'patient', 'rating', 'review', 'created_at']
        read_only_fields = ['id', 'created_at', 'patient']
