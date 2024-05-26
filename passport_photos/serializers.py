from rest_framework import serializers

from .models import PassportPhotoModel


class PassportPhotoSerializer(serializers.ModelSerializer):
    url = serializers.ImageField(required=False)

    class Meta:
        model = PassportPhotoModel
        fields = '__all__'
