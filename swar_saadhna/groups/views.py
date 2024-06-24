from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    AddGroupSerializer,
    GetGroupSerializer,
    GetGroupAudiosSerializer,
    GetGroupUsersSerializer,
    AddGroupAudiosSerializer,
    CreateGroupCodeSerializer,
    JoinGroupSerializer,
)
from .handlers.group import GroupHandlers
from .handlers.group_audios import GroupAudiosHandlers
from .handlers.group_users import GroupUsersHandlers

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
        return GroupHandlers.create_group(validate_data.validated_data, token)


class GroupAudios(APIView):
    def get(self, request):
        validate_data = GetGroupAudiosSerializer(data=request.query_params)
        if not validate_data.is_valid():
            return Response(validate_data.errors, status.HTTP_422_UNPROCESSABLE_ENTITY)
        token = request.headers.get("Authorization")
        return GroupAudiosHandlers.get_group_audios(validate_data.validated_data, token)

    def post(self, request):
        validate_data = AddGroupAudiosSerializer(data=request.data)
        if not validate_data.is_valid():
            return Response(validate_data.errors, status.HTTP_422_UNPROCESSABLE_ENTITY)
        token = request.headers.get("Authorization")
        return GroupAudiosHandlers.add_group_audios(validate_data.validated_data, token)


class GroupUsers(APIView):
    def get(self, request):
        validate_data = GetGroupUsersSerializer(data=request.query_params)
        if not validate_data.is_valid():
            return Response(validate_data.errors, status.HTTP_422_UNPROCESSABLE_ENTITY)
        token = request.headers.get("Authorization")
        return GroupUsersHandlers.get_group_users(validate_data.validated_data, token)


class JoinGroup(APIView):
    def get(self, request):
        validate_data = CreateGroupCodeSerializer(data=request.query_params)
        if not validate_data.is_valid():
            return Response(validate_data.errors, status.HTTP_422_UNPROCESSABLE_ENTITY)
        token = request.headers.get("Authorization")
        return GroupUsersHandlers.generate_grp_pin(validate_data.validated_data, token)

    def post(self, request):
        validate_data = JoinGroupSerializer(data=request.data)
        if not validate_data.is_valid():
            return Response(validate_data.errors, status.HTTP_422_UNPROCESSABLE_ENTITY)
        token = request.headers.get("Authorization")
        return GroupUsersHandlers.join_grp(validate_data.validated_data, token)
