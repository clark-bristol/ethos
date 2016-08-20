from django import forms
from .models import Claim
from django.contrib.auth.models import User


class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['name', 'content', 'source', 'tags']
