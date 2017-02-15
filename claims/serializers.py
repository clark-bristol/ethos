from rest_framework import serializers
from claims.models import Claim, Affirmation
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = ('id', 'name', 'content')


class AffirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affirmation
        fields = ('id', 'claim', 'user')
