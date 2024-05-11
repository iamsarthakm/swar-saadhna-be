from django.contrib.auth.hashers import check_password
from .models import User
from django.core.mail import send_mail
import random


def check_credentials(username, password):
    user = User.objects.filter(username=username, is_deleted=False).first()
    if not user:
        return None, None
    is_valid_password = check_password(password, user.password)
    return is_valid_password, user


def mail_pin_to_user(email, pin):
    send_mail(
        "Swar Saadhan PIN",
        pin,
        "Don't Reply <do_not_reply@swarSaadhna.com>",
        [email],
        fail_silently=False,
    )


def generate_4_digit_pin():
    return str(random.randint(1000, 9999))
