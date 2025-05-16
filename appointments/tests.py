from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from accounts.models import User
from doctors.models import DoctorProfile
from .models import Appointment

class AppointmentCreationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.patient = User.objects.create_user(email='pat@example.com', username='pat', phone='123', user_type='patient', password='pass')
        self.doctor_user = User.objects.create_user(email='doc@example.com', username='doc', phone='456', user_type='doctor', password='pass')
        self.doctor_profile = DoctorProfile.objects.create(user=self.doctor_user, specialty='Cardiology', years_of_experience=5, certification='Cert', degree='MD')
        self.client.force_authenticate(user=self.patient)
        self.url = reverse('appointment-list')
        self.data = {
            'doctor': self.doctor_profile.id,
            'date': '2025-05-20',
            'time': '10:00',
            'status': 'booked',
            'severity': 'mild',
            'symptoms': 'cough',
        }

    def test_appointment_creation_sends_notification(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Appointment.objects.filter(doctor=self.doctor_profile, patient=self.patient).exists())
