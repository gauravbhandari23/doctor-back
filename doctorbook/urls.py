"""
URL configuration for doctorbook project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from accounts.token_views import MyTokenObtainPairView
from accounts.views import UserViewSet, PasswordResetRequestView, PasswordResetConfirmView
from accounts.registration_views import UserRegistrationView, EmailVerificationView
from doctors.views import DoctorProfileViewSet, DoctorAvailabilityViewSet
from doctors.views_rating import DoctorRatingViewSet
from patients.views import PatientProfileViewSet
from appointments.views import AppointmentViewSet
from notifications.views import NotificationViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'doctors', DoctorProfileViewSet)
router.register(r'doctor-availabilities', DoctorAvailabilityViewSet)
router.register(r'patients', PatientProfileViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'doctor-ratings', DoctorRatingViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', UserRegistrationView.as_view(), name='user_register'),
    path('api/password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('api/password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('api/verify-email/', EmailVerificationView.as_view(), name='verify_email'),
]
