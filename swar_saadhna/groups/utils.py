import jwt
from django.conf import settings


def get_user_id_from_token(request):
    token = request.headers.get("Authorization")
    payload = jwt.decode(
        token, settings.JWT_SECRET_KEY, verify=True, algorithms=["HS256"]
    )
    return payload.get("id", None)
