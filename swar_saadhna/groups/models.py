from django.db import models
from users.models import User
from score_sound.models import AudioScore


# class GroupPermission(models.Model):
#     name = models.CharField(max_length=255)


# class GroupRole(models.Model):
#     name = models.CharField(max_length=255)


# class GroupRolesAndPermission(models.Model):
#     role = models.ForeignKey(GroupPermission, on_delete=models.CASCADE)
#     permission = models.ForeignKey(GroupPermission, on_delete=models.CASCADE)


class Group(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


class GroupAudio(models.Model):
    audio = models.ForeignKey(AudioScore, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
