from django.db import models
from django.conf import settings
from transactions.models import Category

class Budget(models.Model):
    """
    Budget limits for spending categories
    """
    PERIOD_CHOICES = (
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='budgets'
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        related_name='budgets'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    alert_threshold = models.IntegerField(
        default=80,
        help_text="Alert when budget reaches this percentage (default 80%)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'category', 'period', 'start_date']
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.category.name} - ${self.amount}/{self.period}"