from django.db import models
from django.conf import settings
from .models import DoctorProfile

class DoctorProfileAuditLog(models.Model):
    doctor_profile = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='audit_logs')
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    change_type = models.CharField(max_length=20)  # e.g., 'created', 'updated'
    timestamp = models.DateTimeField(auto_now_add=True)
    changes = models.TextField()  # JSON or string description of changes

    def __str__(self):
        return f"{self.doctor_profile} - {self.change_type} at {self.timestamp}"
