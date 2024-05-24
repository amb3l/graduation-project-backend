from django.contrib.auth import authenticate

from rest_framework import serializers

from .models import UserModel


class RegistrationSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = UserModel(**validated_data)
        user.set_password(password)
        user.save()

        return user

    class Meta:
        model = UserModel
        fields = ('id', 'name', 'email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'max_length': 128,
                'min_length': 8,
            }
        }


class LoginSerializer(serializers.ModelSerializer):
    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(email, password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'id': user.id,
            'name': user.name,
            'email': user.email,
        }

    class Meta:
        model = UserModel
        fields = ('id', 'name', 'email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'max_length': 128,
                'min_length': 8,
            }
        }
