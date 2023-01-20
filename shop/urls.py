from django.urls import path
from .views import Cars, Parts, create_part, parts_by_category

urlpatterns = [
    path('cars/', Cars.as_view(), name='cars'),
    path('parts/', Parts.as_view(), name='parts'),
    path('part/create/', create_part, name='create-parts'),
    path('parts/<str:category>', parts_by_category, name='parts-by-category'),
]