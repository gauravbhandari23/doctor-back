from django.test import TestCase
from .models import DoctorProfile
from accounts.models import User

class DoctorProfileModelTest(TestCase):
    def test_create_doctor_profile(self):
        user = User.objects.create_user(email='doc@example.com', username='doc', phone='123', user_type='doctor', password='pass')
        profile = DoctorProfile.objects.create(user=user, specialty='Cardiology', years_of_experience=5, certification='Cert', degree='MD')
        self.assertEqual(profile.user.email, 'doc@example.com')
        self.assertEqual(profile.specialty, 'Cardiology')

    def test_rating_update(self):
        user = User.objects.create_user(email='doc2@example.com', username='doc2', phone='456', user_type='doctor', password='pass')
        profile = DoctorProfile.objects.create(user=user, specialty='Dermatology', years_of_experience=3, certification='Cert2', degree='MBBS')
        # Initial rating
        self.assertEqual(profile.rating, 0.0)
        self.assertEqual(profile.rating_count, 0)
        # Simulate ratings: 5, 4, 3
        ratings = [5, 4, 3]
        for r in ratings:
            total = profile.rating * profile.rating_count
            profile.rating_count += 1
            profile.rating = (total + r) / profile.rating_count
            profile.save()
        self.assertAlmostEqual(profile.rating, 4.0)
        self.assertEqual(profile.rating_count, 3)
