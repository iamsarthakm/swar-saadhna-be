import jwt
from django.conf import settings
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
import logging
import time
from django.utils.deprecation import MiddlewareMixin

req_logger = logging.getLogger("django.request")
logger = logging.getLogger(__name__)


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


# class GlobalExceptionMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)
#         return response

#     def process_exception(self, request, exception):
#         logger.error(f"Unhandled exception: {exception}", exc_info=True)
#         return Response(
#             {"data": None, "message": "An unexpected error occurred."}, status=500
#         )


class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        response_time = time.time() - request.start_time
        self.log_response(request, response, response_time)
        return response

    def log_response(self, request, response, response_time):
        try:
            body = request.body.decode("utf-8")
        except Exception:
            body = "Unable to decode body"
        req_logger.info(
            f"""
            Method: {request.method}
            Path: {request.get_full_path()}
            Body: {body}
            Params: {request.GET.dict()}
            Response Status Code: {response.status_code}
            Response Time: {response_time} seconds
        """
        )
