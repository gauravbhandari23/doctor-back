from django.db import models
from accounts.models import User
from doctors.models import DoctorProfile

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('booked', 'Booked'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    )
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'patient'})
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='booked')
    severity = models.CharField(max_length=50)
    symptoms = models.TextField()

    def __str__(self):
        return f"{self.doctor.user.email} - {self.patient.email} - {self.date} {self.time}"