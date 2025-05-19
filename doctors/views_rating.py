from rest_framework import viewsets, permissions
from .models_rating import DoctorRating
from .serializers_rating import DoctorRatingSerializer
from .models import DoctorProfile
from accounts.models import User
from django.db.models import Avg

class DoctorRatingViewSet(viewsets.ModelViewSet):
    queryset = DoctorRating.objects.all()
    serializer_class = DoctorRatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Ensure patient is the logged-in user
        instance = serializer.save(patient=self.request.user)
        self._update_doctor_rating(instance.doctor)

    def perform_update(self, serializer):
        instance = serializer.save()
        self._update_doctor_rating(instance.doctor)

    def perform_destroy(self, instance):
        doctor = instance.doctor
        instance.delete()
        self._update_doctor_rating(doctor)

    def _update_doctor_rating(self, doctor):
        ratings = doctor.ratings.all()
        count = ratings.count()
        avg = ratings.aggregate(Avg('rating'))['rating__avg'] or 0.0
        doctor.rating = avg
        doctor.rating_count = count
        doctor.save()
