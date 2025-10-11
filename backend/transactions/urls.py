from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, TransactionViewSet, RecurringTransactionViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('transactions', TransactionViewSet, basename='transaction')
router.register('recurring', RecurringTransactionViewSet, basename='recurring-transaction')

urlpatterns = [
    path('', include(router.urls)),
]