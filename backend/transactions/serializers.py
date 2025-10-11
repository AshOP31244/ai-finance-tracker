from rest_framework import serializers
from .models import Category, Transaction, RecurringTransaction

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    Handles both default categories and user-created custom categories.
    """
    class Meta:
        model = Category
        fields = ('id', 'name', 'type', 'icon', 'color', 'is_default', 'created_at')
        read_only_fields = ('id', 'is_default', 'created_at')
    
    def create(self, validated_data):
        """
        When creating a category, automatically assign it to the logged-in user.
        The user comes from the request context.
        """
        validated_data['user'] = self.context['request'].user
        validated_data['is_default'] = False  # User-created categories are never default
        return super().create(validated_data)


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for Transaction model.
    Includes extra fields to show category details without making extra database queries.
    """
    # These fields pull data from the related Category object
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_icon = serializers.CharField(source='category.icon', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    
    class Meta:
        model = Transaction
        fields = (
            'id', 'amount', 'type', 'category', 'category_name', 
            'category_icon', 'category_color', 'date', 'description', 
            'is_recurring', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def validate(self, attrs):
        """
        Custom validation: Make sure the amount is positive.
        """
        if attrs.get('amount') and attrs['amount'] <= 0:
            raise serializers.ValidationError({"amount": "Amount must be greater than 0."})
        return attrs
    
    def create(self, validated_data):
        """
        When creating a transaction, automatically assign it to the logged-in user.
        """
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class RecurringTransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for RecurringTransaction model.
    Used for transactions that repeat on a schedule like monthly rent.
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = RecurringTransaction
        fields = (
            'id', 'amount', 'type', 'category', 'category_name', 
            'description', 'frequency', 'next_date', 'is_active', 'created_at'
        )
        read_only_fields = ('id', 'created_at')
    
    def create(self, validated_data):
        """
        Automatically assign recurring transaction to the logged-in user.
        """
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)