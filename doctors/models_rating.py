from django.db import models
from accounts.models import User
from .models import DoctorProfile

class DoctorRating(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='ratings')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_ratings')
    rating = models.PositiveSmallIntegerField()  # 1-5
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('doctor', 'patient')  # One rating per patient per doctor

    def __str__(self):
        return f"{self.doctor.user.email} rated {self.rating} by {self.patient.email}"
