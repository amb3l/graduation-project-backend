from rest_framework import serializers

from .models import UserModel


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = UserModel(**validated_data)
        user.save()

        return user

    class Meta:
        model = UserModel
        fields = ('id', 'name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
