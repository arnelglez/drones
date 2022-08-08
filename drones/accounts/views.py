from email.mime import image
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from django.utils.translation import  gettext_lazy as _

from django.contrib.auth import authenticate

# rest-framework api imports
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.models import User
from .serializers import UserSerializer, UserCustomSerializer, CustomTokenObtainPairSerializer


class Login(TokenObtainPairView):
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(
            username=username,
            password=password
        )
        
        if user:
            loginSerializer = CustomTokenObtainPairSerializer(data=request.data)
            if loginSerializer.is_valid():
                userSerializer = UserCustomSerializer(user)
                response = {
                    "token": loginSerializer.validated_data.get('access'),
                    "referesh": loginSerializer.validated_data.get('refresh'),
                    "user" : userSerializer.data
                }
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
        return JsonResponse(_('failed username or password'), safe=False, status=status.HTTP_400_BAD_REQUEST)
        

class Logout(TokenObtainPairView):
    
    def post(self, request):
        user = get_object_or_404(User, id=request.data.get('user'))
        if user.exists():
            RefreshToken.for_user(user)
            return JsonResponse(_('Seccion close correctly'), safe=False, status=status.HTTP_200_OK) 
        return JsonResponse(_('User not exist'), safe=False, status=status.HTTP_400_BAD_REQUEST) 
        
        