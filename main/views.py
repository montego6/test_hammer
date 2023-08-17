from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response


class LoginGetCodeView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        return Response({'phone_nuber': phone_number})

@login_required
def index(request):
    return HttpResponse('Profile page')



# Create your views here.
