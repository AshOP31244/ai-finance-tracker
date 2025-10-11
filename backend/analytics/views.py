from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Avg, Count, Q
from django.db.models.functions import TruncDate, TruncMonth
from datetime import datetime, timedelta
from transactions.models import Transaction
import pandas as pd

class AnalyticsInsightsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        today = datetime.now().date()
        three_months_ago = today - timedelta(days=90)
        
        transactions = Transaction.objects.filter(
            user=user,
            date__gte=three_months_ago
        )
        
        if not transactions.exists():
            return Response({
                'insights': [],
                'message': 'Not enough data for insights'
            })
        
        insights = []
        
        # Average spending analysis
        avg_monthly_expense = transactions.filter(
            type='expense'
        ).values('date__month').annotate(
            total=Sum('amount')
        ).aggregate(avg=Avg('total'))['avg'] or 0
        
        current_month_expense = transactions.filter(
            type='expense',
            date__month=today.month,
            date__year=today.year
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        if current_month_expense > avg_monthly_expense * 1.2:
            insights.append({
                'type': 'warning',
                'title': 'Higher Spending This Month',
                'message': f'Your spending is ${current_month_expense - avg_monthly_expense:.2f} above your 3-month average.',
                'icon': '⚠️'
            })
        elif current_month_expense < avg_monthly_expense * 0.8:
            insights.append({
                'type': 'success',
                'title': 'Great Savings!',
                'message': f'You\'re spending ${avg_monthly_expense - current_month_expense:.2f} less than usual this month.',
                'icon': '🎉'
            })
        
        # Top spending category
        top_category = transactions.filter(
            type='expense'
        ).values('category__name').annotate(
            total=Sum('amount')
        ).order_by('-total').first()
        
        if top_category:
            total_expense = transactions.filter(type='expense').aggregate(
                total=Sum('amount')
            )['total'] or 0
            
            percentage = (top_category['total'] / total_expense * 100) if total_expense > 0 else 0
            
            insights.append({
                'type': 'info',
                'title': 'Biggest Spending Category',
                'message': f'{top_category["category__name"]} accounts for {percentage:.1f}% of your expenses (${top_category["total"]:.2f}).',
                'icon': '📊'
            })
        
        # Savings rate
        total_income = transactions.filter(type='income').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        total_expense = transactions.filter(type='expense').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        if total_income > 0:
            savings_rate = ((total_income - total_expense) / total_income) * 100
            
            if savings_rate >= 20:
                insights.append({
                    'type': 'success',
                    'title': 'Excellent Savings Rate',
                    'message': f'You\'re saving {savings_rate:.1f}% of your income. Keep it up!',
                    'icon': '💰'
                })
            elif savings_rate < 10:
                insights.append({
                    'type': 'warning',
                    'title': 'Low Savings Rate',
                    'message': f'You\'re only saving {savings_rate:.1f}% of your income. Consider reducing expenses.',
                    'icon': '💡'
                })
        
        return Response({
            'insights': insights,
            'generated_at': today.isoformat()
        })


class SpendingPredictionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        today = datetime.now().date()
        six_months_ago = today - timedelta(days=180)
        
        monthly_expenses = Transaction.objects.filter(
            user=user,
            type='expense',
            date__gte=six_months_ago
        ).annotate(
            month=TruncMonth('date')
        ).values('month').annotate(
            total=Sum('amount')
        ).order_by('month')
        
        if len(monthly_expenses) < 2:
            return Response({
                'prediction': None,
                'message': 'Need at least 2 months of data for prediction'
            })
        
        amounts = [float(m['total']) for m in monthly_expenses]
        avg_expense = sum(amounts) / len(amounts)
        
        if len(amounts) >= 3:
            recent_avg = sum(amounts[-3:]) / 3
            trend_percentage = ((recent_avg / avg_expense) - 1) * 100
        else:
            recent_avg = avg_expense
            trend_percentage = 0
        
        predicted_amount = recent_avg * (1 + (trend_percentage / 100))
        
        return Response({
            'prediction': {
                'predicted_amount': round(predicted_amount, 2),
                'confidence': 'medium' if len(amounts) >= 4 else 'low',
                'trend': 'increasing' if trend_percentage > 5 else 'decreasing' if trend_percentage < -5 else 'stable',
                'trend_percentage': round(trend_percentage, 1)
            },
            'historical_average': round(avg_expense, 2),
            'data_points': len(amounts)
        })


class SpendingComparisonView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        today = datetime.now().date()
        current_month_start = today.replace(day=1)
        
        current_month_data = Transaction.objects.filter(
            user=user,
            date__gte=current_month_start
        ).aggregate(
            income=Sum('amount', filter=Q(type='income')),
            expenses=Sum('amount', filter=Q(type='expense'))
        )
        
        if today.month == 1:
            prev_month_start = today.replace(year=today.year - 1, month=12, day=1)
        else:
            prev_month_start = today.replace(month=today.month - 1, day=1)
        
        prev_month_end = current_month_start - timedelta(days=1)
        
        prev_month_data = Transaction.objects.filter(
            user=user,
            date__range=[prev_month_start, prev_month_end]
        ).aggregate(
            income=Sum('amount', filter=Q(type='income')),
            expenses=Sum('amount', filter=Q(type='expense'))
        )
        
        current_income = float(current_month_data['income'] or 0)
        current_expenses = float(current_month_data['expenses'] or 0)
        prev_income = float(prev_month_data['income'] or 0)
        prev_expenses = float(prev_month_data['expenses'] or 0)
        
        income_change = ((current_income - prev_income) / prev_income * 100) if prev_income > 0 else 0
        expense_change = ((current_expenses - prev_expenses) / prev_expenses * 100) if prev_expenses > 0 else 0
        
        return Response({
            'current_month': {
                'income': current_income,
                'expenses': current_expenses,
                'savings': current_income - current_expenses
            },
            'previous_month': {
                'income': prev_income,
                'expenses': prev_expenses,
                'savings': prev_income - prev_expenses
            },
            'changes': {
                'income_change_percentage': round(income_change, 2),
                'expense_change_percentage': round(expense_change, 2),
                'income_direction': 'up' if income_change > 0 else 'down' if income_change < 0 else 'same',
                'expense_direction': 'up' if expense_change > 0 else 'down' if expense_change < 0 else 'same'
            }
        })