from rest_framework.response import Response
from rest_framework import status
from ..utils import get_user_id_from_token
from ..models import Group, UserGroup
from django.db.models import Q, Count


class GroupHandlers:

    def create_group(data, token):
        user_id = get_user_id_from_token(token)
        # TODO these transactions should be atomic
        group = Group.objects.create(name=data["name"])
        UserGroup.objects.create(user_id=user_id, group=group, role="admin")
        return Response(
            {"data": None, "message": "Group created successfully"},
            status.HTTP_200_OK,
        )

    def get_user_group_details(params, token):
        user_id = get_user_id_from_token(token)
        search = params["search"]
        limit = params["limit"]
        offset = params["offset"]
        qf = Q(is_deleted=False, usergroup__user_id=user_id)
        if search != "":
            qf = Q(name__icontains=search)
        groups_data = (
            Group.objects.filter(qf)
            .annotate(
                num_users=Count("usergroup", filter=Q(usergroup__is_deleted=False)),
                num_audios=Count("groupaudio", filter=Q(groupaudio__is_deleted=False)),
            )
            .values("id", "name", "num_users", "num_audios", "usergroup__role")
        )[limit : limit + offset]
        output = []

        # Append group details to output list
        for group in groups_data:
            group_info = {
                "id": group["id"],
                "name": group["name"],
                "users_count": group["num_users"],
                "audios_count": group["num_audios"],
                "role": group["usergroup__role"],
            }
            output.append(group_info)

        return Response(
            {"data": output, "message": None},
            status.HTTP_200_OK,
        )
