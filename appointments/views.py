from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdminOrReadOnly
from .models import Appointment
from .serializers import AppointmentSerializer
from django.core.mail import send_mail
from django.conf import settings
from notifications.models import Notification

# Create your views here.

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

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
            # Notify doctor
            Notification.objects.create(
                recipient=appointment.doctor.user,
                message=f"New appointment booked by {user.username} for {appointment.date} at {appointment.time}.",
                appointment=appointment
            )
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
        instance = self.get_object()
        prev_status = instance.status
        # Prevent patients from changing the patient field
        if user.user_type == 'patient' and not user.is_staff:
            updated = serializer.save(patient=user)
        # Prevent doctors from changing the doctor field
        elif user.user_type == 'doctor' and not user.is_staff:
            doctor_profile = getattr(user, 'doctor_profile', None)
            if doctor_profile:
                updated = serializer.save(doctor=doctor_profile)
            else:
                updated = serializer.save()
        else:
            updated = serializer.save()
        # Notify patient if doctor confirms appointment
        if prev_status == 'pending' and updated.status == 'confirmed':
            Notification.objects.create(
                recipient=updated.patient,
                message=f"Your appointment on {updated.date} at {updated.time} has been confirmed by Dr. {updated.doctor.user.username}.",
                appointment=updated
            )
        # Notify patient if doctor completes appointment
        if prev_status in ['pending', 'confirmed'] and updated.status == 'completed':
            Notification.objects.create(
                recipient=updated.patient,
                message=f"Your appointment on {updated.date} at {updated.time} with Dr. {updated.doctor.user.username} has been marked as completed. Thank you for visiting!",
                appointment=updated
            )
        # Notify doctor if patient cancels appointment
        if user.user_type == 'patient' and not user.is_staff:
            if prev_status != 'canceled' and updated.status == 'canceled':
                Notification.objects.create(
                    recipient=updated.doctor.user,
                    message=f"The appointment on {updated.date} at {updated.time} with {updated.patient.username} has been canceled by the patient.",
                    appointment=updated
                )
            # Notify doctor if patient edits (date, time, severity, symptoms) and not a cancel
            elif updated.status == prev_status and (
                instance.date != updated.date or
                instance.time != updated.time or
                instance.severity != updated.severity or
                instance.symptoms != updated.symptoms
            ):
                Notification.objects.create(
                    recipient=updated.doctor.user,
                    message=f"The appointment on {updated.date} at {updated.time} with {updated.patient.username} has been updated by the patient.",
                    appointment=updated
                )
        # Send notification/email (placeholder)
        send_mail(
            'Appointment Updated',
            f'Appointment details: {updated}',
            settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@example.com',
            [updated.doctor.user.email, updated.patient.email],
            fail_silently=True,
        )

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
