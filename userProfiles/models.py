"""
Extend the existing User model (which only deals with authentication etc)
Source: https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#extending-the-existing-user-model
"""
from django.db import models
from django.contrib.auth.models import User

class StandardUser(models.Model):
    user = models.OneToOneField(User)
    authority = models.IntegerField(default=0)