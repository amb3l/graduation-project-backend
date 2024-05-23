from rest_framework import serializers

from .models import CoordinateModel, PlatformModel


class CoordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoordinateModel
        fields = '__all__'


class PlatformSerializer(serializers.ModelSerializer):
    coordinates = CoordinateSerializer(many=True)

    def create(self, validated_data):
        coordinates = validated_data.pop('coordinates')
        platform = PlatformModel.objects.create(**validated_data)

        for coordinate in coordinates:
            coordinate, created = CoordinateModel.objects.get_or_create(x=coordinate['x'], y=coordinate['y'])
            platform.ingredients.add(coordinate)

        return platform

    class Meta:
        model = PlatformModel
        fields = ('id', 'name', 'city', 'address', 'coordinates')
