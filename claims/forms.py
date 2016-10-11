from django import forms
from .models import Claim, Argument
# from django.contrib.auth.models import User


class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['name', 'content']


class ArgumentForm(forms.ModelForm):
    class Meta:
        model = Argument
        fields = ['name', 'supported_claim', 'premise_claims']
        widgets = {
            'premise_claims': forms.CheckboxSelectMultiple()
        }
