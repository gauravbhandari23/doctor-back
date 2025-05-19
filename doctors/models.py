from django.db import models
from accounts.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import json
from django.core.mail import send_mail
from django.conf import settings

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialty = models.CharField(max_length=100)
    years_of_experience = models.PositiveIntegerField()
    certification = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    profile_photo = models.ImageField(upload_to='doctor_photos/', null=True, blank=True)
    clinic_location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    certificate_document = models.FileField(upload_to='doctor_certificates/', null=True, blank=True)
    # New fields for rating
    rating = models.FloatField(default=0.0)
    rating_count = models.PositiveIntegerField(default=0)
    # TODO: Add admin verification workflow logic here if required in the future
    # TODO: Add doctor availability/slots model and relation if needed
    # TODO: Add more fields for advanced search/filter if needed
    # TODO: Add notification/email logic on profile update if needed in the future
    # TODO: Add audit logging for profile changes if required in the future
    # TODO: Add signals for post-save actions (e.g., send verification email)

    def __str__(self):
        return f"{self.user.email} - {self.specialty} (Rating: {self.rating:.2f} from {self.rating_count} ratings)"

class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='availabilities')
    day_of_week = models.CharField(max_length=10, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot_duration_minutes = models.PositiveIntegerField(default=30)

    def __str__(self):
        return f"{self.doctor.user.email} - {self.day_of_week} {self.start_time}-{self.end_time}"

    class Meta:
        unique_together = ('doctor', 'day_of_week', 'start_time', 'end_time')

class DoctorProfileAuditLog(models.Model):
    doctor_profile = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='audit_logs')
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    change_type = models.CharField(max_length=20)  # e.g., 'created', 'updated'
    changes = models.TextField()  # JSON string of changes
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.doctor_profile.user.email} - {self.change_type} at {self.timestamp}"

@receiver(post_save, sender=DoctorProfile)
def log_doctor_profile_change(sender, instance, created, **kwargs):
    change_type = 'created' if created else 'updated'
    changes = {}
    for field in instance._meta.fields:
        value = getattr(instance, field.name)
        try:
            json.dumps(value)
        except TypeError:
            value = str(value)
        changes[field.name] = value
    try:
        DoctorProfileAuditLog.objects.create(
            doctor_profile=instance,
            changed_by=getattr(instance.user, 'last_modified_by', None),  # Placeholder, can be improved
            change_type=change_type,
            changes=json.dumps(changes)
        )
    except Exception as e:
        import logging
        logging.error(f"Failed to create DoctorProfileAuditLog: {e}")

@receiver(post_save, sender=DoctorProfile)
def send_doctor_profile_notification(sender, instance, created, **kwargs):
    subject = 'Doctor Profile Created' if created else 'Doctor Profile Updated'
    message = f"Dear {instance.user.email}, your doctor profile has been {subject.lower()}."
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@example.com',
        [instance.user.email],
        fail_silently=True,
    )