from django.urls import path
from django.views.generic import TemplateView
from . views import index, LoginGetCodeView, LoginView, logout_view, GetUserProfileView


urlpatterns = [
    path('', index, name='index'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login-page'),
    path('logout/', logout_view, name='logout'),
    path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile-page'),
    path('api/login/code/', LoginGetCodeView.as_view(), name='api-login-code'),
    path('api/login/', LoginView.as_view(), name='api-login'),
    path('api/profile/', GetUserProfileView.as_view(), name='api-profile'),
    ]