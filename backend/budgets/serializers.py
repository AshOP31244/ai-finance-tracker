from rest_framework import serializers
from .models import Budget
from transactions.models import Transaction
from django.db.models import Sum
from datetime import datetime

class BudgetSerializer(serializers.ModelSerializer):
    """
    Serializer for Budget model.
    Includes calculated fields that show how much of the budget has been spent.
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    # These are calculated fields that don't exist in the database
    # They're computed on-the-fly when the data is serialized
    spent_amount = serializers.SerializerMethodField()
    remaining_amount = serializers.SerializerMethodField()
    percentage_used = serializers.SerializerMethodField()
    
    class Meta:
        model = Budget
        fields = (
            'id', 'category', 'category_name', 'amount', 'period', 
            'start_date', 'end_date', 'is_active', 'alert_threshold',
            'spent_amount', 'remaining_amount', 'percentage_used',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_spent_amount(self, obj):
        """
        Calculate how much money has been spent in this budget's category
        during the budget period.
        """
        spent = Transaction.objects.filter(
            user=obj.user,
            category=obj.category,
            type='expense',
            date__range=[obj.start_date, obj.end_date]
        ).aggregate(total=Sum('amount'))['total']
        
        return float(spent or 0)
    
    def get_remaining_amount(self, obj):
        """
        Calculate how much money is left in the budget.
        """
        spent = self.get_spent_amount(obj)
        return float(obj.amount) - spent
    
    def get_percentage_used(self, obj):
        """
        Calculate what percentage of the budget has been used.
        This is used to show progress bars and trigger alerts.
        """
        spent = self.get_spent_amount(obj)
        if obj.amount > 0:
            return round((spent / float(obj.amount)) * 100, 2)
        return 0
    
    def validate(self, attrs):
        """
        Make sure the end date comes after the start date.
        """
        if attrs.get('start_date') and attrs.get('end_date'):
            if attrs['start_date'] >= attrs['end_date']:
                raise serializers.ValidationError(
                    {"end_date": "End date must be after start date."}
                )
        return attrs
    
    def create(self, validated_data):
        """
        Automatically assign budget to the logged-in user.
        """
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)