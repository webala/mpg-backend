from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import permission_classes 
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import MyTokenObtainPairSerializer, NewUserSerializer

# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = NewUserSerializer

class MyTokenObtainView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer