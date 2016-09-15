from rest_framework import serializers
from claims.models import Claim, Affirmation
from django.contrib.auth.models import User


# automatically generate serializer class (http://www.django-rest-framework.org/tutorial/1-serialization/)
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class ClaimSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(many=False, view_name='user-detail', read_only=True)
    class Meta:
        model = Claim
        fields = ('id', 'name', 'content', 'user')


class AffirmationSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(many=False, view_name='user-detail', read_only=True)
    claim = serializers.HyperlinkedRelatedField(many=False, view_name='claim-detail', read_only=True)

    class Meta:
        model = Affirmation
        fields = ('id','user', 'claim')
