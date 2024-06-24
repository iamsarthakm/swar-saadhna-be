from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    SendOTPSerializer,
    VerifyOTPSerializer,
)
from .handlers import UserHandlers


# Create your views here.


class Register(APIView):
    def post(self, request):
        validate_data = UserRegisterSerializer(data=request.data)
        if not validate_data.is_valid():
            return Response(validate_data.errors, status.HTTP_422_UNPROCESSABLE_ENTITY)
        return UserHandlers.save(validate_data.validated_data)


class Login(APIView):
    def get(self, request):
        validate_data = UserLoginSerializer(data=request.query_params)
        if not validate_data.is_valid():
            return Response(validate_data.errors, status.HTTP_422_UNPROCESSABLE_ENTITY)
        return UserHandlers.login(validate_data.validated_data)


class SendOTP(APIView):
    def get(self, request):
        validate_data = SendOTPSerializer(data=request.query_params)
        if not validate_data.is_valid():
            return Response(validate_data.errors, status.HTTP_422_UNPROCESSABLE_ENTITY)
        return UserHandlers.send_otp(validate_data.validated_data)


class VerifyOTP(APIView):
    def post(self, request):
        validate_data = VerifyOTPSerializer(data=request.data)
        if not validate_data.is_valid():
            return Response(validate_data.errors, status.HTTP_422_UNPROCESSABLE_ENTITY)
        return UserHandlers.verify_otp(validate_data.validated_data)
