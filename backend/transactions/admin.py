from django.contrib import admin
from .models import Category, Transaction, RecurringTransaction

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'user', 'is_default', 'color', 'icon']
    list_filter = ['type', 'is_default']
    search_fields = ['name']
    ordering = ['type', 'name']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'type', 'category', 'date', 'created_at']
    list_filter = ['type', 'category', 'date']
    search_fields = ['description', 'user__email']
    date_hierarchy = 'date'
    ordering = ['-date', '-created_at']

@admin.register(RecurringTransaction)
class RecurringTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'type', 'frequency', 'next_date', 'is_active']
    list_filter = ['frequency', 'is_active', 'type']
    search_fields = ['description', 'user__email']
    ordering = ['next_date']