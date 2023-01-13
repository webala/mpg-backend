from django.urls import path
from .views import Cars, Parts

urlpatterns = [
    path('cars/', Cars.as_view(), name='cars'),
    path('parts/', Parts.as_view(), name='parts')
]