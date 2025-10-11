from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Q, Avg
from datetime import datetime, timedelta
from .models import Transaction, Category, RecurringTransaction
from .serializers import (
    TransactionSerializer, 
    CategorySerializer, 
    RecurringTransactionSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Category operations.
    Automatically provides: list, create, retrieve, update, destroy
    
    Additional custom actions:
    - expense_categories: Get only expense categories
    - income_categories: Get only income categories
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return categories that either:
        1. Belong to the logged-in user (custom categories), OR
        2. Are default categories (available to everyone)
        """
        return Category.objects.filter(
            Q(user=self.request.user) | Q(is_default=True)
        )
    
    @action(detail=False, methods=['get'])
    def expense_categories(self, request):
        """
        Custom endpoint: GET /api/transactions/categories/expense_categories/
        Returns only expense-type categories.
        """
        categories = self.get_queryset().filter(type='expense')
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def income_categories(self, request):
        """
        Custom endpoint: GET /api/transactions/categories/income_categories/
        Returns only income-type categories.
        """
        categories = self.get_queryset().filter(type='income')
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)


class TransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Transaction operations.
    Provides full CRUD operations plus custom analytics endpoints.
    """
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return only transactions belonging to the logged-in user.
        Also supports filtering via query parameters.
        """
        queryset = Transaction.objects.filter(user=self.request.user)
        
        # Filter by transaction type (expense or income)
        transaction_type = self.request.query_params.get('type')
        if transaction_type:
            queryset = queryset.filter(type=transaction_type)
        
        # Filter by category
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])
        
        return queryset
    
    def perform_create(self, serializer):
        """
        When creating a transaction, automatically set the user.
        This is called automatically by the create action.
        """
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Custom endpoint: GET /api/transactions/transactions/summary/
        
        Returns financial summary for a given period:
        - Total income
        - Total expenses
        - Net savings
        - Savings rate
        - Category breakdown
        
        Query params:
        - start_date: Start of period (default: first day of current month)
        - end_date: End of period (default: today)
        """
        queryset = self.get_queryset()
        
        # Get date range from query parameters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if not start_date or not end_date:
            # Default to current month
            today = datetime.now().date()
            start_date = today.replace(day=1)
            end_date = today
        
        # Filter transactions to the date range
        queryset = queryset.filter(date__range=[start_date, end_date])
        
        # Calculate total income
        total_income = queryset.filter(type='income').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        # Calculate total expenses
        total_expenses = queryset.filter(type='expense').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        # Get spending breakdown by category
        category_breakdown = queryset.filter(type='expense').values(
            'category__name', 'category__icon', 'category__color'
        ).annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')
        
        # Calculate savings metrics
        net_savings = total_income - total_expenses
        savings_rate = (net_savings / total_income * 100) if total_income > 0 else 0
        
        return Response({
            'period': {
                'start_date': start_date,
                'end_date': end_date
            },
            'total_income': float(total_income),
            'total_expenses': float(total_expenses),
            'net_savings': float(net_savings),
            'savings_rate': round(savings_rate, 2),
            'category_breakdown': list(category_breakdown),
            'transaction_count': queryset.count()
        })
    
    @action(detail=False, methods=['get'])
    def trends(self, request):
        """
        Custom endpoint: GET /api/transactions/transactions/trends/
        
        Returns monthly spending/income trends over the last 6 months.
        Used for displaying line charts showing financial trends over time.
        """
        # Get last 6 months of data
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=180)
        
        queryset = self.get_queryset().filter(date__range=[start_date, end_date])
        
        # Group transactions by month
        from django.db.models.functions import TruncMonth
        monthly_data = queryset.annotate(
            month=TruncMonth('date')
        ).values('month', 'type').annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('month')
        
        # Format the data into a more frontend-friendly structure
        formatted_data = {}
        for item in monthly_data:
            month_key = item['month'].strftime('%Y-%m')
            
            if month_key not in formatted_data:
                formatted_data[month_key] = {
                    'month': month_key,
                    'income': 0,
                    'expenses': 0,
                    'net': 0
                }
            
            # Add income or expenses to the month
            if item['type'] == 'income':
                formatted_data[month_key]['income'] = float(item['total'])
            else:
                formatted_data[month_key]['expenses'] = float(item['total'])
            
            # Calculate net (income - expenses)
            formatted_data[month_key]['net'] = (
                formatted_data[month_key]['income'] - 
                formatted_data[month_key]['expenses']
            )
        
        return Response({
            'trends': list(formatted_data.values())
        })
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        Custom endpoint: GET /api/transactions/transactions/recent/
        
        Returns the 10 most recent transactions.
        Used for displaying a "Recent Transactions" widget on the dashboard.
        """
        queryset = self.get_queryset()[:10]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RecurringTransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for RecurringTransaction operations.
    Handles transactions that repeat on a schedule (rent, subscriptions, etc.)
    """
    serializer_class = RecurringTransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return only recurring transactions belonging to the logged-in user.
        """
        return RecurringTransaction.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """
        Automatically set the user when creating a recurring transaction.
        """
        serializer.save(user=self.request.user)