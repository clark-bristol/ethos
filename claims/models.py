from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
# for tags (http://django-taggit.readthedocs.org/en/latest/getting_started.html)
# from taggit.managers import TaggableManager


# Create your models here.
class Claim(models.Model):
    name = models.CharField(max_length=120, blank=False, null=True)
    content = models.CharField(max_length=1000, blank=False, null=True)
    creator_user = models.ForeignKey(User, on_delete=models.CASCADE)
    # source = models.CharField(max_length=120, blank=False, null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    # user = models.CharField(max_length=120, blank=False, null=True)
    # num_affirmations = models.IntegerField(blank=False, default=0)
    # tags = TaggableManager()  # http://django-taggit.readthedocs.org/en/latest/getting_started.html


# Create your models here.
class Affirmation(models.Model):
    claim = models.ForeignKey(Claim)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        unique_together = ('claim', 'user')
