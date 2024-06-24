from django.contrib.auth.hashers import check_password
from .models import User
from django.core.mail import send_mail
import random
import boto3
from botocore.exceptions import BotoCoreError, ClientError
import jwt
import requests
from django.conf import settings
import re
from swar_saadhna.utils import CustomException
from django.core.cache import cache


def check_credentials(username, password):
    user = User.objects.filter(username=username, is_deleted=False).first()
    if not user:
        return None, None
    is_valid_password = check_password(password, user.password)
    return is_valid_password, user


def send_pin_to_user(username, pin):
    username_type = is_email_or_phone(username)
    if username_type == "email":
        send_mail(
            "Swar Saadhan PIN",
            pin,
            "Don't Reply <do_not_reply@swarSaadhna.com>",
            [username],
            fail_silently=False,
        )

    elif username_type == "phone":
        pass
        # response = send_pass_to_user(token, username)
        # send_sms(username, f"The pin for your login is {pin}")
    else:
        raise CustomException("Please enter correct username")


def generate_4_digit_pin():
    return str(random.randint(1000, 9999))


# def store_otp(phone_number, otp):
#     # TODO store it in redis later on
#     cache.set(phone_number, otp, timeout=300)


def send_sms(phone_number, message):
    try:
        sns_client = boto3.client(
            "sns",
            region_name=settings.REGION_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        sns_client.publish(PhoneNumber=phone_number, Message=message)
    except (BotoCoreError, ClientError) as error:
        print(f"Error sending SMS: {error}")


# def verify_otp(phone_number, otp):
#     stored_otp = cache.get(phone_number)
#     return stored_otp == otp


def is_email_or_phone(input_string):
    # Define regex patterns
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    phone_pattern = r"^\+?[1-9]\d{1,14}$"  # E.164 format: + followed by 1-15 digits

    # Check if the input_string matches the email pattern
    if re.match(email_pattern, input_string):
        return "email"

    # Check if the input_string matches the phone pattern
    if re.match(phone_pattern, input_string):
        return "phone"

    # If it matches neither pattern
    return "invalid"


def get_user_id_from_token(request):
    token = request.headers.get("Authorization")
    payload = jwt.decode(
        token, settings.JWT_SECRET_KEY, verify=True, algorithms=["HS256"]
    )
    return payload.get("id", None)


def get_message_token():
    token = cache.get("msg_token")
    if token is None:
        token = get_message_verification_token()
        set_token(token)
    return token


def set_token(token):
    timeout_7_days = 7 * 24 * 60 * 60
    cache.set("user_token", token, timeout=timeout_7_days)


def get_message_verification_token():
    url = "https://cpaas.messagecentral.com/auth/v1/authentication/token?country=IN&customerId=C-DE251B4119374E5&key=JTt9ckUuN144TyU4wqM=&scope=NEW"
    payload = {}
    headers = {"accept": "*/*"}
    response = requests.request("GET", url, headers=headers, data=payload)
    timeout_seconds = 7 * 24 * 60 * 60
    cache.set("auth-msg-token", response.json()["token"], timeout_seconds)
    return response.json()["token"]


def send_otp_to_user(phone_number):
    url = f"https://cpaas.messagecentral.com/verification/v2/verification/send?countryCode=91&customerId={settings.MC_CUSTOMER_ID}&flowType=SMS&mobileNumber={phone_number}"

    payload = {}
    token = get_auth_msg_token()
    headers = {"authToken": token}

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.json())
    return response.json()["data"]["verificationId"]


def verify_otp(phone_number, otp, verification_id):
    print(phone_number, otp, verification_id)
    url = f"https://cpaas.messagecentral.com/verification/v2/verification/validateOtp?countryCode=91&mobileNumber={phone_number}&verificationId={verification_id}&customerId={settings.MC_CUSTOMER_ID}&code={otp}"

    payload = {}
    token = get_auth_msg_token()
    headers = {"authToken": token}

    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.json())
    return response.json()["responseCode"]


def get_auth_msg_token():
    if token := cache.get("auth-msg-token"):
        return token
    else:
        return get_message_verification_token()
