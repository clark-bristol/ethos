from rest_framework import serializers
from claims.models import Claim


# create your serializers here
# class ClaimSerializer(serializers.Serializer):
#     name = serializers.CharField(required=True, max_length=120, allow_blank=False)
#     content = serializers.CharField(required=False, max_length=1000, allow_blank=False)
#     source = serializers.CharField(required=False, max_length=120, allow_blank=False)
#     user_id = serializers.IntegerField(required=False)
#     user = serializers.CharField(required=False, max_length=120, allow_blank=False)
#     votes = serializers.IntegerField(required=False)

# automatically generate serializer class (http://www.django-rest-framework.org/tutorial/1-serialization/)
class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = ('name', 'content', 'source', 'user_id', 'votes', 'user')
