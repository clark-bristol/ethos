from rest_framework import serializers
from claims.models import Claim, Affirmation


# automatically generate serializer class (http://www.django-rest-framework.org/tutorial/1-serialization/)
class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = ('name', 'content', 'contrib_user_id', 'affirmations')


class AffirmationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affirmation
        fields = ('user', 'claim')
