# Concerned that deleting a claim will not be prevented if it's in an argument.
# probably need to create an explicit through table for this
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
# for tags (http://django-taggit.readthedocs.org/en/latest/getting_started.html)
# from taggit.managers import TaggableManager


# Create your models here.
class Claim(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField(max_length=10000)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    # tags = TaggableManager()  # http://django-taggit.readthedocs.org/en/latest/getting_started.html

    class Meta:
        unique_together = ('name', 'content')

    def __str__(self):
        return "(%s) %s" % (self.id, self.name)
    def __unicode__(self):
        return "(%s) %s" % (self.id, self.name)



# Create your models here.
class Affirmation(models.Model):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        unique_together = ('claim', 'user')


# Create your models here.
class Argument(models.Model):
    name = models.CharField(max_length=255)
    premise_claims = models.ManyToManyField(Claim, through='ArgumentPremise')
    supported_claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name='supporting_arguments')
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        unique_together = ('name', 'supported_claim')


# Create your models here.
class ArgumentPremise(models.Model):
    argument = models.ForeignKey(Argument, on_delete=models.CASCADE)
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        unique_together = ('argument', 'claim')
