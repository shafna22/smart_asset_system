from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Employee', 'Employee'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Employee')

    
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'Admin'
        super().save(*args, **kwargs)