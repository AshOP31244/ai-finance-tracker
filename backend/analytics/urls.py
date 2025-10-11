from django.urls import path
from .views import AnalyticsInsightsView, SpendingPredictionView, SpendingComparisonView

urlpatterns = [
    path('insights/', AnalyticsInsightsView.as_view(), name='analytics-insights'),
    path('prediction/', SpendingPredictionView.as_view(), name='spending-prediction'),
    path('comparison/', SpendingComparisonView.as_view(), name='spending-comparison'),
]