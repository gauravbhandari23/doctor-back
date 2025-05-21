from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdminOrReadOnly
from .permissions import IsOwnerOrAdminOrReadOnly
from .models import DoctorProfile, DoctorAvailability
from .serializers import DoctorProfileSerializer, DoctorAvailabilitySerializer

# Create your views here.
# No router registration here. All router registration is handled in doctorbook/urls.py.


from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

class DoctorProfileViewSet(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['specialty', 'clinic_location', 'user__email']
    ordering_fields = ['years_of_experience', 'is_verified']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.user_type == 'doctor' and not user.is_staff:
            return queryset.filter(user=user)
        # Allow patients to see all doctors
        # Advanced filter by query params
        specialty = self.request.query_params.get('specialty')
        is_verified = self.request.query_params.get('is_verified')
        location = self.request.query_params.get('clinic_location')
        if specialty:
            queryset = queryset.filter(specialty__icontains=specialty)
        if is_verified is not None:
            queryset = queryset.filter(is_verified=(is_verified.lower() == 'true'))
        if location:
            queryset = queryset.filter(clinic_location__icontains=location)
        return queryset

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    @transaction.atomic
    def rate(self, request, pk=None):
        """
        Allows a patient to rate a doctor. Expects 'rating' in POST data (1-5).
        """
        doctor = self.get_object()
        rating = request.data.get('rating')
        try:
            rating = float(rating)
        except (TypeError, ValueError):
            return Response({'detail': 'Invalid rating value.'}, status=status.HTTP_400_BAD_REQUEST)
        if not (1 <= rating <= 5):
            return Response({'detail': 'Rating must be between 1 and 5.'}, status=status.HTTP_400_BAD_REQUEST)
        # Update average rating
        total = doctor.rating * doctor.rating_count
        doctor.rating_count += 1
        doctor.rating = (total + rating) / doctor.rating_count
        doctor.save()
        return Response({'detail': 'Rating submitted.', 'rating': doctor.rating, 'rating_count': doctor.rating_count})

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        # Allow all authenticated users to view (GET, HEAD, OPTIONS) doctor profiles
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            return obj
        # Only allow staff or the doctor themselves to update/delete
        if user.is_staff:
            return obj
        if user.user_type == 'doctor' and obj.user == user:
            return obj
        from rest_framework.exceptions import PermissionDenied
        raise PermissionDenied('You do not have permission to modify this doctor profile.')

    def update(self, request, *args, **kwargs):
        data = request.data.copy()
        data.pop('user', None)
        data.pop('user_email', None)
        # Ensure other fields are included in the update
        request._full_data = data  # For DRF 3.12+ compatibility
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        data = request.data.copy()
        data.pop('user', None)
        data.pop('user_email', None)
        # Ensure other fields are included in the partial update
        request._full_data = data  # For DRF 3.12+ compatibility
        return super().partial_update(request, *args, **kwargs)

class DoctorAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = DoctorAvailability.objects.all()
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'doctor' and not user.is_staff:
            return DoctorAvailability.objects.filter(doctor__user=user)
        return super().get_queryset()

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if user.is_staff:
            return obj
        if user.user_type == 'doctor' and obj.doctor.user == user:
            return obj
        # Otherwise, permission denied
        from rest_framework.exceptions import PermissionDenied
        raise PermissionDenied('You do not have permission to access this object.')
