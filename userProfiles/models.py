"""
Extend the existing User model (which only deals with authentication etc)
Source:
	https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#extending-the-existing-user-model
Solved problem of user not getting created (expands on mysterious last sentence of above link):
	http://stackoverflow.com/questions/28748281/extending-user-profile-in-django-1-7
"""
from django.db import models
from django.contrib.auth.models import User
from claims.models import Claim

class StandardUser(models.Model):
    user = models.OneToOneField(User)
    authority = models.IntegerField(default=0)
    #ADD LIST OF AFFIRMED CLAIMS https://docs.djangoproject.com/en/1.9/ref/models/fields/#model-field-types
    # affirms = models.ManyToManyField(Claim)