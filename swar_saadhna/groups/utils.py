import jwt
from django.conf import settings
from .models import UserGroup, GroupAudio
from score_sound.utils.utils import generate_presigned_url


def get_user_id_from_token(token):
    # token = request.headers.get("Authorization")
    payload = jwt.decode(
        token, settings.JWT_SECRET_KEY, verify=True, algorithms=["HS256"]
    )
    return payload.get("id", None)


def add_users_to_group(
    user_id,
    group_id,
    role="member",
):
    # group_users = [
    #     UserGroup(user_id=user_id, group_id=group_id, role=role) for user_id in user_ids
    # ]
    # UserGroup.objects.bulk_create(group_users)
    UserGroup.objects.get_or_create(
        user_id=user_id, group_id=group_id, role=role, is_deleted=False
    )


def add_audios_to_group(audio_ids, group_id):
    # group_audios = [
    #     GroupAudio(audio_id=audio_id, group_id=group_id) for audio_id in audio_ids
    # ]
    for audio_id in audio_ids:
        GroupAudio.objects.get_or_create(
            audio_id=audio_id, group_id=group_id, is_deleted=False
        )


def get_group_audios_util(group_id, limit, offset, search):
    group_audios_data = (
        GroupAudio.objects.select_related("audio")
        .filter(group_id=group_id, audio__name__icontains=search, is_deleted=False)
        .values(
            "audio__id",
            "audio__name",
            "audio__tempo",
            "audio__scale",
            "audio__audio_url",
        )
    )[limit : limit + offset]
    output = []
    for group_audio in group_audios_data:
        output.append(
            {
                "id": group_audio["audio__id"],
                "name": group_audio["audio__name"],
                "tempo": group_audio["audio__tempo"],
                "scale": group_audio["audio__scale"],
                "url": generate_presigned_url(group_audio["audio__audio_url"]),
            }
        )
    return output


def get_group_users_util(group_id, limit, offset, search):
    group_users_data = (
        UserGroup.objects.select_related("user")
        .filter(group_id=group_id, user__username__icontains=search, is_deleted=False)
        .values("user__id", "user__username")
    )[limit : limit + offset]
    out = []
    for group_user in group_users_data:
        out.append(
            {
                "id": group_user["user__id"],
                "name": group_user["user__username"],
            }
        )
    return out
