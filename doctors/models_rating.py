from django.db import models
from accounts.models import User
from .models import DoctorProfile
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg

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

@receiver([post_save, post_delete], sender=DoctorRating)
def update_doctor_profile_rating(sender, instance, **kwargs):
    doctor = instance.doctor
    ratings = doctor.ratings.all()
    count = ratings.count()
    avg = ratings.aggregate(Avg('rating'))['rating__avg'] or 0.0
    doctor.rating = avg
    doctor.rating_count = count
    doctor.save()
