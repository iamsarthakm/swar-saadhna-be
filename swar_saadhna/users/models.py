from django.db import models
from django.contrib.auth.models import User


class BaseUser(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10, null=True)
    email = models.EmailField(max_length=255, null=True)


class SavedMedia(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    storage_url = models.URLField()
