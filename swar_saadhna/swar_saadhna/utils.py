from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


class CustomException(APIException):
    detail = None

    def __init__(self, detail):
        super().__init__(detail)
        self.detail = detail


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and "detail" in response.data:
        response.data["message"] = response.data["detail"]
        del response.data["detail"]
    return response
