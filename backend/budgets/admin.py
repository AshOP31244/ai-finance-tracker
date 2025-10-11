from django.contrib import admin
from .models import Budget

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'amount', 'period', 'start_date', 'end_date', 'is_active']
    list_filter = ['period', 'is_active']
    search_fields = ['user__email', 'category__name']
    date_hierarchy = 'start_date'
    ordering = ['-start_date']