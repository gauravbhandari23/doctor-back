from rest_framework import serializers
from .models import DoctorProfile, DoctorAvailability


class DoctorProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField(read_only=True)
    user_phone = serializers.SerializerMethodField(read_only=True)
    user_username = serializers.SerializerMethodField(read_only=True)
    rating = serializers.FloatField(read_only=True)
    rating_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = DoctorProfile
        fields = [
            'id', 'user', 'user_email', 'user_phone', 'user_username',
            'specialty', 'years_of_experience', 'certification', 'degree',
            'profile_photo', 'certificate_document', 'clinic_location',
            'latitude', 'longitude', 'is_verified',
            'rating', 'rating_count',
        ]
        read_only_fields = ['user', 'user_email', 'user_phone', 'user_username', 'rating', 'rating_count']

    def get_user_email(self, obj):
        return obj.user.email if obj.user else ''

    def get_user_phone(self, obj):
        return obj.user.phone if obj.user else ''

    def get_user_username(self, obj):
        return obj.user.username if obj.user else ''

    def update(self, instance, validated_data):
        # Update related user phone if present in request
        user = instance.user
        request = self.context.get('request')
        if request and 'user_phone' in request.data:
            user.phone = request.data['user_phone']
            user.save()
        return super().update(instance, validated_data)

class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailability
        fields = ['id', 'doctor', 'day_of_week', 'start_time', 'end_time', 'slot_duration_minutes']
