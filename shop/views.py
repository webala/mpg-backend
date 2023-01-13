from django.shortcuts import render
from rest_framework import generics
from .models import Car, Part
from .serializers import CarSerializer, PartsSerializer

# Create your views here.

class Cars(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

class Parts(generics.ListCreateAPIView):
    queryset = Part.objects.all()
    serializer_class = PartsSerializer