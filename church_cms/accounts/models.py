from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    birthday = models.DateField(null=True)
    is_member = models.BooleanField(null=True, default=False)


class Device(models.Model):
    token = models.CharField(unique=True, max_length=255)
    os_version = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=255)
    model = models.CharField(max_length=100)
    resolution = models.CharField(max_length=50)
    screen_height = models.CharField(max_length=50)
    screen_width = models.CharField(max_length=50)
    app_version = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class DeviceConsent(models.Model):
    push_broadcast = models.BooleanField(default=True)
    app_notification = models.BooleanField(default=True)
    email = models.BooleanField(default=True)
    device = models.OneToOneField(Device, on_delete=models.CASCADE, primary_key=True, related_name='consent')
