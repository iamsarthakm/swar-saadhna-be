from django.db import models
from users.models import User

# Create your models here.


class Composition(models.Model):
    name = models.CharField(max_length=255)
    notes_and_beats = models.JSONField()
    details = models.JSONField(null=True)
    rhythm = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


class AudioScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    scale = models.CharField(max_length=20)
    tempo = models.IntegerField()
    composition = models.ForeignKey(Composition, on_delete=models.CASCADE)
    audio_url = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


class Taal(models.Model):
    name = models.CharField(max_length=255)
    beats = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
