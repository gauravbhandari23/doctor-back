from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdminOrReadOnly
from .models import PatientProfile
from .serializers import PatientProfileSerializer

class PatientProfileViewSet(viewsets.ModelViewSet):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'patient' and not user.is_staff:
            return PatientProfile.objects.filter(user=user)
        return super().get_queryset()
