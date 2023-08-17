from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from .models import LoginCode
from .funcs import generate_login_code

class LoginGetCodeView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        code = generate_login_code()
        code_instance = LoginCode.objects.create(code=code, phone_number=phone_number, expires_at=datetime.now() + timedelta(minutes=1))
        return Response({'phone_nuber': phone_number, 'code': code_instance.code})


class LoginView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        code = request.data.get
        if not phone_number:
            return Response({'error': 'phone_number should be provided'}, status=status.HTTP_400_BAD_REQUEST)
        if not code:
            return Response({'error': 'code should be provided'}, status=status.HTTP_400_BAD_REQUEST)
        

@login_required
def index(request):
    return HttpResponse('Profile page')



# Create your views here.
