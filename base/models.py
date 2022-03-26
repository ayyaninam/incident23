from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Raised(models.Model):
    creation_date_time = models.DateTimeField(blank=True, null=True)
    resolution_date_time = models.DateTimeField(blank=True, null=True)
    res_time = models.CharField(max_length=100, blank=True, null=True)
    priority = models.CharField(max_length=300, blank=True, null=True)
    urgency = models.CharField(max_length=300, blank=True, null=True)
    assigned_organization = models.CharField(
        max_length=500, blank=True, null=True)
    inc_type = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.resolution_date_time


class Closed(models.Model):
    creation_date_time = models.DateTimeField(blank=True, null=True)
    resolution_date_time = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.creation_date_time


class Backlog(models.Model):
    priority = models.CharField(max_length=300, blank=True, null=True)
    inc_type = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.inc_type


class ExcelFileUpload(models.Model):
    excel_file_upload = models.FileField(upload_to='excel')
