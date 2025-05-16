from django.db import models
from accounts.models import User

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    medical_history = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.email