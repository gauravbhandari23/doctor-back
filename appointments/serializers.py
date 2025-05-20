from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(read_only=True)
    doctor_name = serializers.SerializerMethodField()
    patient_name = serializers.SerializerMethodField()
    patient_email = serializers.SerializerMethodField()
    patient_phone = serializers.SerializerMethodField()
    patient_medical_history = serializers.SerializerMethodField()
    patient_allergies = serializers.SerializerMethodField()
    patient_chronic_conditions = serializers.SerializerMethodField()
    patient_current_medications = serializers.SerializerMethodField()
    patient_blood_type = serializers.SerializerMethodField()
    patient_gender = serializers.SerializerMethodField()
    patient_date_of_birth = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = [
            'id', 'doctor', 'doctor_name', 'patient', 'patient_name', 'patient_email', 'patient_phone',
            'patient_medical_history', 'patient_allergies', 'patient_chronic_conditions',
            'patient_current_medications', 'patient_blood_type', 'patient_gender', 'patient_date_of_birth',
            'date', 'time', 'status', 'severity', 'symptoms'
        ]

    def get_doctor_name(self, obj):
        return obj.doctor.user.full_name if obj.doctor and obj.doctor.user else ""

    def get_patient_name(self, obj):
        return obj.patient.full_name if obj.patient else ""

    def get_patient_email(self, obj):
        return obj.patient.email if obj.patient else ""

    def get_patient_phone(self, obj):
        return obj.patient.phone if obj.patient else ""

    def get_patient_medical_history(self, obj):
        return getattr(getattr(obj.patient, 'patient_profile', None), 'medical_history', '')

    def get_patient_allergies(self, obj):
        return getattr(getattr(obj.patient, 'patient_profile', None), 'allergies', '')

    def get_patient_chronic_conditions(self, obj):
        return getattr(getattr(obj.patient, 'patient_profile', None), 'chronic_conditions', '')

    def get_patient_current_medications(self, obj):
        return getattr(getattr(obj.patient, 'patient_profile', None), 'current_medications', '')

    def get_patient_blood_type(self, obj):
        return getattr(getattr(obj.patient, 'patient_profile', None), 'blood_type', '')

    def get_patient_gender(self, obj):
        return getattr(getattr(obj.patient, 'patient_profile', None), 'gender', '')

    def get_patient_date_of_birth(self, obj):
        dob = getattr(getattr(obj.patient, 'patient_profile', None), 'date_of_birth', None)
        return dob.isoformat() if dob else ''
