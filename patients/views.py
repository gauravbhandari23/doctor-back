from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from accounts.permissions import IsOwnerOrAdmin
from .models import PatientProfile
from .serializers import PatientProfileSerializer
import logging

logger = logging.getLogger(__name__)

class PatientProfileViewSet(viewsets.ModelViewSet):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'patient' and not user.is_staff:
            return PatientProfile.objects.filter(user=user)
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        user = self.request.user
        if user.user_type == 'patient' and not user.is_staff:
            instance = self.get_object()
            if instance.user != user:
                return Response({'detail': 'You do not have permission to update this profile.'}, status=403)
        return super().partial_update(request, *args, **kwargs)

    @action(detail=False, methods=['get', 'patch'], url_path='me')
    def me(self, request):
        user = request.user
        try:
            patient_profile = PatientProfile.objects.get(user=user)
            if request.method == 'PATCH':
                logger.info('Incoming PATCH payload: %s', request.data)
                serializer = self.get_serializer(patient_profile, data=request.data, partial=True)
                if not serializer.is_valid():
                    logger.error('Validation errors: %s', serializer.errors)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            serializer = self.get_serializer(patient_profile)
            return Response(serializer.data)
        except PatientProfile.DoesNotExist:
            return Response({'detail': 'Patient profile not found.'}, status=404)
