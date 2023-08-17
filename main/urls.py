from django.urls import path
from django.views.generic import TemplateView
from . views import index, LoginGetCodeView


urlpatterns = [
    path('', index, name='index'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login-page'),
    path('api/login/get-code/', LoginGetCodeView.as_view(), name='api-login-code'),
    ]