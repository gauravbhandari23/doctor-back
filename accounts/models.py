from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('admin', 'Admin'),
    )
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone', 'user_type']