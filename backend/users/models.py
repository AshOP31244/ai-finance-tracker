from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom User Model that extends Django's default User
    Adds additional fields for personal finance tracking
    """
    email = models.EmailField(unique=True)
    monthly_income = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="User's monthly income for budget calculations"
    )
    currency = models.CharField(
        max_length=3, 
        default='USD',
        help_text="Currency code (USD, EUR, INR, etc.)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Use email as the unique identifier for login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'