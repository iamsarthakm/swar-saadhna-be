from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    AddGroupSerializer,
    GetGroupSerializer,
)
from .handlers import GroupHandlers

# Create your views here.


class Group(APIView):
    def get(self, request):
        validate_data = GetGroupSerializer(data=request.query_params)
        if not validate_data.is_valid():
            return Response(validate_data.errors, status.HTTP_422_UNPROCESSABLE_ENTITY)
        token = request.headers.get("Authorization")
        return GroupHandlers.get_user_group_details(validate_data.validated_data, token)

    def post(self, request):
        validate_data = AddGroupSerializer(data=request.data)
        if not validate_data.is_valid():
            return Response(validate_data.errors, status.HTTP_422_UNPROCESSABLE_ENTITY)
        token = request.headers.get("Authorization")
        return GroupHandlers.add_group(validate_data.validated_data, token)
