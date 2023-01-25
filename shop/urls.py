from django.urls import path
from .views import Cars, Parts, parts_by_category, PartDetail

urlpatterns = [
    path('cars/', Cars.as_view(), name='cars'),
    path('parts/', Parts.as_view(), name='parts'),
    path('part/<pk>', PartDetail.as_view(), name='part'),
    path('parts/<str:category>', parts_by_category, name='parts-by-category'),
]