from django.shortcuts import redirect
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
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
        code_instance = LoginCode(code=code, phone_number=phone_number, expires_at=datetime.now() + timedelta(minutes=1))
        try:
            code_instance.full_clean()
        except ValidationError:
            return Response({'status': 'error', 'detail': 'invalid phone number, should be 7XXXXXXXXXX'})
        else:
            code_instance.save()
        return Response({
            'status': 'success',
            'detail': 'code sent',
            'phone_number': phone_number, 
            'code': code_instance.code}, 
            status=status.HTTP_200_OK)


class LoginView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')
        
        if not phone_number:
            return Response({'status': 'error', 'detail': 'phone_number should be provided'}, status=status.HTTP_400_BAD_REQUEST)
        if not code:
            return Response({'status': 'error', 'detail': 'code should be provided'}, status=status.HTTP_400_BAD_REQUEST)
        
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
        else:
            return Response({'status': 'error', 'detail': 'such code does not exist or is expired'})


class GetUserProfileView(APIView):
    def get(self, request):
        user = request.user
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response({'status': 'error', 'detail': 'profile does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class GetInvitedView(APIView):
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'status': 'error', 'detail': 'you must login'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            user_profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response({'status': 'error', 'detail': 'profile for this user does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            if user_profile.code_invited:
                return Response({'status': 'error', 'detail': 'you have already activated invite code'}, status=status.HTTP_403_FORBIDDEN)
        
        invite_code = request.data.get('invite_code')
        if not invite_code:
            return Response({'status': 'error', 'detail': 'code not provided'}, status=status.HTTP_400_BAD_REQUEST)
        if not Profile.objects.filter(invite_code=invite_code).exists():
            return Response({'status': 'error', 'detail': 'profile with such code does not exist'}, status=status.HTTP_403_FORBIDDEN)
        
        profile = Profile.objects.get(invite_code=invite_code)
        profile.invited_users.add(user)
        Profile.objects.filter(user=request.user).update(code_invited=invite_code)
        return Response({'status': 'success', 
                         'detail': 'invite code accepted'
                         }, status=status.HTTP_200_OK)


@login_required
def index(request):
    return redirect('profile-page')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login-page')


# Create your views here.
