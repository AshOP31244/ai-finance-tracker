from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from datetime import datetime, timedelta
from .models import Budget
from .serializers import BudgetSerializer
from transactions.models import Transaction

class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Budget.objects.filter(user=self.request.user)
        
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        period = self.request.query_params.get('period')
        if period:
            queryset = queryset.filter(period=period)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def overview(self, request):
        today = datetime.now().date()
        active_budgets = self.get_queryset().filter(
            is_active=True,
            start_date__lte=today,
            end_date__gte=today
        )
        
        budget_data = []
        alerts = []
        
        for budget in active_budgets:
            serializer = self.get_serializer(budget)
            data = serializer.data
            
            percentage_used = data['percentage_used']
            if percentage_used >= 100:
                alerts.append({
                    'type': 'danger',
                    'category': data['category_name'],
                    'message': f"Budget exceeded by ${abs(data['remaining_amount']):.2f}"
                })
            elif percentage_used >= budget.alert_threshold:
                alerts.append({
                    'type': 'warning',
                    'category': data['category_name'],
                    'message': f"{percentage_used:.0f}% of budget used"
                })
            
            budget_data.append(data)
        
        return Response({
            'budgets': budget_data,
            'alerts': alerts,
            'total_budgets': len(budget_data)
        })
    
    @action(detail=False, methods=['post'])
    def create_monthly_budgets(self, request):
        today = datetime.now().date()
        start_date = today.replace(day=1)
        
        if today.month == 12:
            end_date = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end_date = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        
        categories_data = request.data.get('categories', [])
        created_budgets = []
        
        for cat_data in categories_data:
            budget, created = Budget.objects.get_or_create(
                user=request.user,
                category_id=cat_data['category_id'],
                period='monthly',
                start_date=start_date,
                defaults={
                    'amount': cat_data['amount'],
                    'end_date': end_date,
                    'is_active': True
                }
            )
            if created:
                created_budgets.append(budget)
        
        serializer = self.get_serializer(created_budgets, many=True)
        return Response({
            'message': f'{len(created_budgets)} budgets created',
            'budgets': serializer.data
        }, status=status.HTTP_201_CREATED)