from django.urls import path
from . import views

urlpatterns = [
    path("register", views.Register.as_view()),
    path("login", views.Login.as_view()),
    path("send-otp", views.SendOTP.as_view()),
    path("verify-otp", views.VerifyOTP.as_view()),
]
