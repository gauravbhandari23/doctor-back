from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import smart_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from .models import User
from .serializers import UserSerializer, EmailVerificationSerializer
from doctors.models import DoctorProfile
from patients.models import PatientProfile

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_verified=False)
        # Automatically create DoctorProfile if user_type is doctor
        if user.user_type == 'doctor':
            DoctorProfile.objects.get_or_create(
                user=user,
                defaults={
                    'specialty': '',
                    'years_of_experience': 0,
                    'certification': '',
                    'degree': '',
                    'clinic_location': '',
                }
            )
        # Automatically create PatientProfile if user_type is patient
        elif user.user_type == 'patient':
            PatientProfile.objects.get_or_create(
                user=user,
                defaults={
                    'medical_history': '',
                }
            )
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = default_token_generator.make_token(user)
        verify_url = f"http://localhost:8000/api/verify-email/?uidb64={uidb64}&token={token}"
        send_mail(
            'Verify your Doctorbook account',
            f'Click the link to verify your account: {verify_url}',
            settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@example.com',
            [user.email],
            fail_silently=True,
        )

class EmailVerificationView(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Account verified successfully.'}, status=status.HTTP_200_OK)
