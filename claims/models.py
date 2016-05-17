from __future__ import unicode_literals
from django.db import models
from taggit.managers import TaggableManager #http://django-taggit.readthedocs.org/en/latest/getting_started.html

# Create your models here.
class Claim(models.Model):
	title = models.CharField(max_length=120, blank=False, null=True)
	claimcontent = models.CharField(max_length=1000, blank=False, null=True)
	source = models.CharField(max_length=120, blank=False, null=True)
	timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)
	updated = models.DateTimeField(auto_now_add=False,auto_now=True)
	user_id = models.IntegerField(blank=False)
	user = models.CharField(max_length=120, blank=False, null=True)
	votes = models.IntegerField(blank=False, default=0)
	tags = TaggableManager() #http://django-taggit.readthedocs.org/en/latest/getting_started.html