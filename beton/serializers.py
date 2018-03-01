from rest_framework import serializers
from beton.models import Userinfo


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Userinfo
        fields = ('username', 'password')