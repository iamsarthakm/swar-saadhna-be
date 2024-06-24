from rest_framework.response import Response
from rest_framework import status
from ..utils import get_user_id_from_token, get_group_audios_util, add_audios_to_group
from ..models import UserGroup
from score_sound.models import AudioScore


class GroupAudiosHandlers:
    def get_group_audios(params, token):
        group_id = params["group_id"]
        search = params["search"]
        limit = params["limit"]
        offset = params["offset"]
        user_id = get_user_id_from_token(token)
        if not UserGroup.objects.filter(
            user_id=user_id, group_id=group_id, is_deleted=False
        ).exists():
            return Response(
                {
                    "data": None,
                    "message": "The group does not exist or you are not part of the group",
                },
                status.HTTP_400_BAD_REQUEST,
            )
        group_audios = get_group_audios_util(group_id, limit, offset, search)
        return Response(
            {
                "data": group_audios,
                "message": None,
            },
            status.HTTP_200_OK,
        )

    def add_group_audios(data, token):
        group_id = data["group_id"]
        audio_ids = data["audio_ids"]
        user_id = get_user_id_from_token(token)
        valid_audio_ids = set(
            AudioScore.objects.filter(
                id__in=audio_ids, user_id=user_id, is_deleted=False
            ).values_list("id", flat=True)
        )
        invalid_audio_ids = set(audio_ids) - valid_audio_ids

        if invalid_audio_ids != set():
            return Response(
                {
                    "data": None,
                    "message": "One or more Audios provided are invalid or not owned by you.",
                },
                status.HTTP_400_BAD_REQUEST,
            )

        if not UserGroup.objects.filter(
            user_id=user_id, group_id=group_id, role="admin", is_deleted=False
        ).exists():
            return Response(
                {
                    "data": None,
                    "message": "The group does not exist or you do not have permission to add audios to group",
                },
                status.HTTP_400_BAD_REQUEST,
            )

        add_audios_to_group(audio_ids, group_id)
        return Response(
            {
                "data": None,
                "message": "Audios added Successfully",
            },
            status.HTTP_200_OK,
        )
