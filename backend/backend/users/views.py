from django.shortcuts import render
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is None or not user.is_active:
            return Response({'detail': 'Invalid credentials'}, status=400)

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        response = Response({'detail': 'Login successful'})

        response.set_cookie(
            key='access_token',
            value=access,
            httponly=True,
            secure=True,  # Set to True in production
            samesite='Lax',
        )

        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=True,  # Set to True in production
            samesite='Lax',
        )

        return response
        
class HomeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({
            'email': request.user.email,
            'username': request.user.username,
        })