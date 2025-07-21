from rest_framework.response import Response
from rest_framework import status
from ..utils import get_user_id_from_token, get_group_users_util, add_users_to_group
from ..models import UserGroup, Group
from users.models import User
import random
from django.core.cache import cache


class GroupUsersHandlers:
    def get_group_users(params, token):
        group_id = params["group_id"]
        search = params["search"]
        limit = params["limit"]
        offset = params["offset"]
        user_id = get_user_id_from_token(token)
        if not UserGroup.objects.filter(
            user_id=user_id, group_id=group_id, role="admin", is_deleted=False
        ).exists():
            return Response(
                {
                    "data": None,
                    "message": "The group does not exist or you do not have permission to view group users",
                },
                status.HTTP_400_BAD_REQUEST,
            )
        group_audios = get_group_users_util(group_id, limit, offset, search)
        return Response(
            {
                "data": group_audios,
                "message": None,
            },
            status.HTTP_200_OK,
        )

    def add_group_users(data, token):
        group_id = data["group_id"]
        user_ids = data["audio_ids"]
        user_id = get_user_id_from_token(token)
        valid_user_ids = set(
            User.objects.filter(id__in=user_ids, is_deleted=False).values_list(
                "id", flat=True
            )
        )
        invalid_user_ids = set(user_ids) - valid_user_ids

        if invalid_user_ids != set():
            return Response(
                {
                    "data": None,
                    "message": "One or more users provided are invalid",
                },
                status.HTTP_400_BAD_REQUEST,
            )

        if not UserGroup.objects.filter(
            user_id=user_id, group_id=group_id, role="admin", is_deleted=False
        ).exists():
            return Response(
                {
                    "data": None,
                    "message": "The group does not exist or you do not have permission to add users to group",
                },
                status.HTTP_400_BAD_REQUEST,
            )

        add_users_to_group(user_ids, group_id)
        return Response(
            {
                "data": None,
                "message": "Users added Successfully",
            },
            status.HTTP_200_OK,
        )

    def generate_grp_pin(data, token):
        group_id = data["group_id"]
        user_id = get_user_id_from_token(token)
        if not UserGroup.objects.filter(
            user_id=user_id, group_id=group_id, role="admin", is_deleted=False
        ).exists():
            return Response(
                {
                    "data": None,
                    "message": "The group does not exist or you do not have permission to add users to group",
                },
                status.HTTP_400_BAD_REQUEST,
            )
        pin = random.randint(100000, 999999)
        timeout_seconds = 15 * 60
        cache.set(pin, group_id, timeout_seconds)
        return Response(
            {
                "data": pin,
                "message": "Valid for 15 min, please ask user to enter the secret code in order to join the group",
            },
            status.HTTP_200_OK,
        )

    def join_grp(data, token):
        # group_id = data["group_id"]
        pin = data["code"]
        user_id = get_user_id_from_token(token)

        group_id = cache.get(pin)
        if not group_id:
            return Response(
                {
                    "data": None,
                    "message": "Wrong pin entered please try again",
                },
                status.HTTP_400_BAD_REQUEST,
            )

        if not Group.objects.filter(id=group_id, is_deleted=False).exists():
            return Response(
                {
                    "data": None,
                    "message": "The group you are trying to join does not exist",
                },
                status.HTTP_400_BAD_REQUEST,
            )

        add_users_to_group(user_id, group_id)

        return Response(
            {
                "data": None,
                "message": "Added to Group Successfully",
            },
            status.HTTP_200_OK,
        )
