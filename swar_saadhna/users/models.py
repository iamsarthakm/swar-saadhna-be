from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=10, null=True)
    email = models.EmailField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
