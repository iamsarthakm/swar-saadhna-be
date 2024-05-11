import jwt
from django.conf import settings
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


def VerifyAuthToken(get_response):
    def middleware(request):
        print("yayaaayay")
        if "register" in request.path or "login" in request.path:
            return get_response(request)
        if not request.headers.get("Authorization"):
            response = custom_error_response("Authorization token not found.")
            return response
        else:
            token = request.headers.get("Authorization")
            try:
                secret_key = settings.JWT_SECRET_KEY
                jwt.decode(token, secret_key, verify=True, algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                return custom_error_response("Token has expired")
            except jwt.InvalidTokenError:
                return custom_error_response("Invalid token")
            except Exception as e:
                return custom_error_response(
                    f"Token verification failed: {e}",
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        response = get_response(request)

        return response

    return middleware


def custom_error_response(message, status=status.HTTP_401_UNAUTHORIZED):
    response = Response({"message": message}, status=status)
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = "application/json"
    response.renderer_context = {}
    response.render()
    return response
