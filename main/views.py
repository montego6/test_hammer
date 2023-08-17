from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from .models import LoginCode, Profile
from .serializers import ProfileSerializer
from .funcs import generate_login_code, generate_invite_code

User = get_user_model()

class LoginGetCodeView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        code = generate_login_code()
        code_instance = LoginCode.objects.create(code=code, phone_number=phone_number, expires_at=datetime.now() + timedelta(minutes=1))
        return Response({
            'status': 'code sent',
            'phone_nuber': phone_number, 
            'code': code_instance.code}, 
            status=status.HTTP_200_OK)


class LoginView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')
        
        if not phone_number:
            return Response({'error': 'phone_number should be provided'}, status=status.HTTP_400_BAD_REQUEST)
        if not code:
            return Response({'error': 'code should be provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        code_db = LoginCode.objects.filter(code=code, phone_number=phone_number, expires_at__gt=datetime.now())
        if code_db.exists():
            user = authenticate(phone_number=phone_number)
            if user is None:
                user = User.objects.create_user(phone_number=phone_number)
                invite_code = generate_invite_code()
                while Profile.objects.filter(invite_code=invite_code).exists():
                    invite_code = generate_invite_code()
                Profile.objects.create(user=user, invite_code=invite_code)
            login(request, user)
            return redirect('profile-page')
        return Response({'login': 'failed'})


class GetUserProfileView(APIView):
    def get(self, request):
        user = request.user
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response({'error': 'profile does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class GetInvitedView(APIView):
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'status': 'error', 'detail': 'you must login'}, status=status.HTTP_401_UNAUTHORIZED)
        
        invite_code = request.data.get('invite_code')
        if not invite_code:
            return Response({'error': 'code not provided'}, status=status.HTTP_400_BAD_REQUEST)
        if not Profile.objects.filter(invite_code=invite_code).exists():
            return Response({'error': 'profile with such code does not exist'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            user_profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response({'status': 'error', 'detail': 'profile for this user does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            if user_profile.code_invited:
                return Response({'status': 'error', 'detail': 'you have already activated invite code'}, status=status.HTTP_403_FORBIDDEN)

        profile = Profile.objects.get(invite_code=invite_code)
        profile.invited_users.add(user)
        Profile.objects.filter(user=request.user).update(code_invited=invite_code)
        return Response({'status': 'success', 
                         'detail': 'invite code succeeded'
                         })


@login_required
def index(request):
    return redirect('profile-page')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login-page')


# Create your views here.
