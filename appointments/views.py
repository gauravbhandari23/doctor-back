from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdminOrReadOnly
from .models import Appointment
from .serializers import AppointmentSerializer
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'patient' and not user.is_staff:
            return Appointment.objects.filter(patient=user)
        if user.user_type == 'doctor' and not user.is_staff:
            return Appointment.objects.filter(doctor__user=user)
        return super().get_queryset()

    def perform_create(self, serializer):
        user = self.request.user
        # If patient is creating, set patient field automatically
        if user.user_type == 'patient' and not user.is_staff:
            appointment = serializer.save(patient=user)
        # If doctor is creating, set doctor field automatically
        elif user.user_type == 'doctor' and not user.is_staff:
            doctor_profile = getattr(user, 'doctor_profile', None)
            if doctor_profile:
                appointment = serializer.save(doctor=doctor_profile)
            else:
                appointment = serializer.save()
        else:
            appointment = serializer.save()
        # Send notification/email (placeholder)
        send_mail(
            'Appointment Booked',
            f'Appointment details: {appointment}',
            settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@example.com',
            [appointment.doctor.user.email, appointment.patient.email],
            fail_silently=True,
        )

    def perform_update(self, serializer):
        user = self.request.user
        # Prevent patients from changing the patient field
        if user.user_type == 'patient' and not user.is_staff:
            serializer.save(patient=user)
        # Prevent doctors from changing the doctor field
        elif user.user_type == 'doctor' and not user.is_staff:
            doctor_profile = getattr(user, 'doctor_profile', None)
            if doctor_profile:
                serializer.save(doctor=doctor_profile)
            else:
                serializer.save()
        else:
            serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        # Only allow patients to delete their own appointments
        if user.user_type == 'patient' and not user.is_staff:
            if instance.patient != user:
                from rest_framework import status
                from rest_framework.response import Response
                return Response({'detail': 'Not allowed to delete this appointment.'}, status=status.HTTP_403_FORBIDDEN)
        # Only allow doctors to delete their own appointments
        elif user.user_type == 'doctor' and not user.is_staff:
            doctor_profile = getattr(user, 'doctor_profile', None)
            if not (doctor_profile and instance.doctor == doctor_profile):
                from rest_framework import status
                from rest_framework.response import Response
                return Response({'detail': 'Not allowed to delete this appointment.'}, status=status.HTTP_403_FORBIDDEN)
        # Admin can delete any
        response = super().destroy(request, *args, **kwargs)
        # TODO: Integrate with notification/email system here if needed
        return response
