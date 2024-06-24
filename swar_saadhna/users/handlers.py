from .models import User
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from .utils import (
    send_pin_to_user,
    generate_4_digit_pin,
    check_credentials,
    send_otp_to_user,
    verify_otp,
)
import jwt
from django.conf import settings
from datetime import datetime, timedelta


class UserHandlers:
    def save(data):
        pin = generate_4_digit_pin()
        user_data = {
            "name": data.get("name"),
            "username": data.get("username"),
            "password": make_password(str(pin)),
            "phone_number": data.get("phone_number"),
            "email": data.get("email"),
        }
        user = User.objects.create(**user_data)
        send_pin_to_user(data.get("username"), pin)
        return Response(
            {"data": user.id, "message": "User saved successfully"}, status.HTTP_200_OK
        )

    def login(data):
        username = data.get("username")
        password = data.get("password")
        is_valid_password, user = check_credentials(username, password)
        if is_valid_password:
            token = jwt.encode(
                {"exp": datetime.utcnow() + timedelta(days=10), "id": user.id},
                settings.JWT_SECRET_KEY,
                algorithm="HS256",
            )
            return Response(
                {"data": token, "message": "credentials ok"},
                status.HTTP_200_OK,
            )
        return Response(
            {"data": None, "message": "wrong credentials"},
            status.HTTP_200_OK,
        )

    def send_otp(data):
        username = data["username"]
        verification_id = send_otp_to_user(username)
        # cache.set(username, verification_id, 4500)
        return Response(
            {"data": {"verification_id": verification_id}, "message": "OTP sent"},
            status.HTTP_200_OK,
        )

    def verify_otp(data):
        username = data["username"]
        otp = data["otp"]
        verification_id = data["verification_id"]
        response_code = verify_otp(username, otp, verification_id)

        if response_code == 200:
            user = get_or_create_user(username)
            token = jwt.encode(
                {"exp": datetime.utcnow() + timedelta(days=10), "id": user.id},
                settings.JWT_SECRET_KEY,
                algorithm="HS256",
            )
            return Response(
                {"data": token, "message": "Login Successful"},
                status.HTTP_200_OK,
            )
        return Response(
            {"data": verification_id, "message": "Wrong otp"},
            status.HTTP_400_BAD_REQUEST,
        )


def get_or_create_user(username):
    user_data = {"username": username}
    user, created = User.objects.get_or_create(**user_data)
    return user


# class UserGroup(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     group = models.ForeignKey(Group, on_delete=models.CASCADE)
#     group_permissions = models.JSONField(default=list)  # Stores group permissions
#     audio_permissions = models.JSONField(default=list)
