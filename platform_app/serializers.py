import json


from rest_framework import serializers

from .models import PlatformModel


class GeoPropertiesSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "name": instance.name,
            "city": instance.city,
            "address": instance.address,
        }

    def create(self, validated_data):
        return validated_data

    class Meta:
        model = PlatformModel
        exclude = ['coordinates']


class GeoPointSerializer(serializers.ModelSerializer):
    coordinates = serializers.ListField(
        child=serializers.FloatField(),
        min_length=2,
        max_length=2,
    )

    def to_representation(self, instance):
        return {
            "type": "Point",
            "coordinates": json.loads(instance.coordinates),
        }

    def create(self, validated_data):
        return validated_data

    class Meta:
        model = PlatformModel
        fields = ['coordinates']


class PlatformSerializer(serializers.Serializer):
    properties = GeoPropertiesSerializer()
    geometry = GeoPointSerializer()

    def to_internal_value(self, data):
        properties = self.fields['properties'].to_internal_value(data['properties'])
        geometry = self.fields['geometry'].to_internal_value(data['geometry'])

        return {
            'name': properties.get('name'),
            'city': properties.get('city'),
            'address': properties.get('address'),
            'coordinates': json.dumps(geometry.get('coordinates')),
        }

    def to_representation(self, instance):
        return {
            "type": "Feature",
            "properties": self.fields['properties'].to_representation(instance),
            "geometry": self.fields['geometry'].to_representation(instance),
        }

    def create(self, validated_data):
        return PlatformModel.objects.create(**validated_data)
