from django.db import models
from users.models import User

# Create your models here.


class AudioScore(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    scale = models.CharField(max_length=20)
    tempo = models.IntegerField()
    rhythm = models.CharField(max_length=255)
    composition = models.JSONField()
    audio_url = models.CharField(max_length=255, null=True)
    misc_info = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


class Taal(models.Model):
    name = models.CharField(max_length=255)
    beats = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
