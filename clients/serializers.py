from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    def create(self, validated_data):
        User = get_user_model()
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'avatar', 'is_male', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
