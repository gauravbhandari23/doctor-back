from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import smart_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import User
from .serializers import UserSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user_model = get_user_model()
        try:
            user = user_model.objects.get(email=email)
        except user_model.DoesNotExist:
            return Response({'detail': 'If the email exists, a reset link will be sent.'}, status=status.HTTP_200_OK)
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        reset_url = f"http://localhost:8000/reset-password-confirm/?uidb64={uidb64}&token={token}"
        send_mail(
            'Password Reset Request',
            f'Use the following link to reset your password: {reset_url}',
            settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@example.com',
            [email],
            fail_silently=True,
        )
        return Response({'detail': 'If the email exists, a reset link will be sent.'}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
