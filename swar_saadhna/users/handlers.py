from .models import User
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from .utils import mail_pin_to_user, generate_4_digit_pin, check_credentials
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
        mail_pin_to_user(data.get("username"), pin)
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
