from django.db import models
from users.models import User
from score_sound.models import AudioScore


class Group(models.Model):
    name = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=False)


class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    group_permissions = models.JSONField(default=list)  # Stores group permissions
    audio_permissions = models.JSONField(default=list)
    is_deleted = models.BooleanField(default=False)


class GroupAudio(models.Model):
    audio = models.ForeignKey(AudioScore, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    is_deleted = models.BooleanField(default=False)
