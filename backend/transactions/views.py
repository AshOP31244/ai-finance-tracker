from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Q, Avg
from django.db.models.functions import TruncMonth
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
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None  # Disable pagination for categories
    
    def get_queryset(self):
        """
        Return categories that either:
        1. Belong to the logged-in user (custom categories), OR
        2. Are default categories (available to everyone)
        """
        user = self.request.user
        return Category.objects.filter(
            Q(user=user) | Q(is_default=True)
        ).order_by('type', 'name')
    
    @action(detail=False, methods=['get'])
    def expense_categories(self, request):
        categories = self.get_queryset().filter(type='expense')
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def income_categories(self, request):
        categories = self.get_queryset().filter(type='income')
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user)
        
        transaction_type = self.request.query_params.get('type')
        if transaction_type:
            queryset = queryset.filter(type=transaction_type)
        
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        queryset = self.get_queryset()
        
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if not start_date or not end_date:
            today = datetime.now().date()
            start_date = today.replace(day=1)
            end_date = today
        
        queryset = queryset.filter(date__range=[start_date, end_date])
        
        total_income = queryset.filter(type='income').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        total_expenses = queryset.filter(type='expense').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        category_breakdown = queryset.filter(type='expense').values(
            'category__name', 'category__icon', 'category__color'
        ).annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')
        
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
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=180)
        
        queryset = self.get_queryset().filter(date__range=[start_date, end_date])
        
        monthly_data = queryset.annotate(
            month=TruncMonth('date')
        ).values('month', 'type').annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('month')
        
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
            
            if item['type'] == 'income':
                formatted_data[month_key]['income'] = float(item['total'])
            else:
                formatted_data[month_key]['expenses'] = float(item['total'])
            
            formatted_data[month_key]['net'] = (
                formatted_data[month_key]['income'] - 
                formatted_data[month_key]['expenses']
            )
        
        return Response({
            'trends': list(formatted_data.values())
        })
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        queryset = self.get_queryset()[:10]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RecurringTransactionViewSet(viewsets.ModelViewSet):
    serializer_class = RecurringTransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return RecurringTransaction.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)