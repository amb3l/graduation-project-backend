from rest_framework import serializers

from .models import PlatformModel


class PlatformSerializer(serializers.ModelSerializer):
    coordinates = serializers.SerializerMethodField()

    def get_coordinates(self):
        x = self.Meta.model.x
        y = self.Meta.model.y

        return [x, y]

    def create(self, validated_data):
        platform = PlatformModel(**validated_data)
        platform.save()

        return platform

    class Meta:
        model = PlatformModel
        fields = ('id', 'name', 'city', 'address', 'coordinates')
