from django.test import TestCase
from .models import DoctorProfile
from accounts.models import User

class DoctorProfileModelTest(TestCase):
    def test_create_doctor_profile(self):
        user = User.objects.create_user(email='doc@example.com', username='doc', phone='123', user_type='doctor', password='pass')
        profile = DoctorProfile.objects.create(user=user, specialty='Cardiology', years_of_experience=5, certification='Cert', degree='MD')
        self.assertEqual(profile.user.email, 'doc@example.com')
        self.assertEqual(profile.specialty, 'Cardiology')
