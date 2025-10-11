from django.core.management.base import BaseCommand
from transactions.models import Category

class Command(BaseCommand):
    help = 'Create default income and expense categories for all users'

    def handle(self, *args, **kwargs):
        # Define expense categories with emojis and colors
        expense_categories = [
            {'name': 'Food & Dining', 'icon': '🍔', 'color': '#EF4444'},
            {'name': 'Transportation', 'icon': '🚗', 'color': '#F59E0B'},
            {'name': 'Shopping', 'icon': '🛍️', 'color': '#EC4899'},
            {'name': 'Entertainment', 'icon': '🎬', 'color': '#8B5CF6'},
            {'name': 'Bills & Utilities', 'icon': '💡', 'color': '#3B82F6'},
            {'name': 'Healthcare', 'icon': '🏥', 'color': '#10B981'},
            {'name': 'Education', 'icon': '📚', 'color': '#6366F1'},
            {'name': 'Personal Care', 'icon': '💇', 'color': '#F472B6'},
            {'name': 'Travel', 'icon': '✈️', 'color': '#14B8A6'},
            {'name': 'Other Expenses', 'icon': '📝', 'color': '#6B7280'},
        ]
        
        # Define income categories
        income_categories = [
            {'name': 'Salary', 'icon': '💰', 'color': '#10B981'},
            {'name': 'Freelance', 'icon': '💼', 'color': '#3B82F6'},
            {'name': 'Investment', 'icon': '📈', 'color': '#8B5CF6'},
            {'name': 'Gift', 'icon': '🎁', 'color': '#EC4899'},
            {'name': 'Other Income', 'icon': '💵', 'color': '#6B7280'},
        ]
        
        created_count = 0
        
        # Create expense categories
        for cat_data in expense_categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                type='expense',
                is_default=True,
                defaults={
                    'icon': cat_data['icon'],
                    'color': cat_data['color'],
                    'user': None  # Default categories don't belong to any user
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created expense category: {cat_data["name"]}')
                )
        
        # Create income categories
        for cat_data in income_categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                type='income',
                is_default=True,
                defaults={
                    'icon': cat_data['icon'],
                    'color': cat_data['color'],
                    'user': None
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created income category: {cat_data["name"]}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✅ Successfully created {created_count} default categories!')
        )