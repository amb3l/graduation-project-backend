from django.contrib.auth import authenticate

from rest_framework import serializers

from .models import UserModel

GET_UNAUTHORIZED_FIELDS = (
    'id',
    'name',
    'email',
    'last_login',
    'date_joined',
)


class ConfirmPassportSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('passport_photo',)


class GetUserByIdSerializer(serializers.ModelSerializer):
    @staticmethod
    def get(validated_data):
        return validated_data

    class Meta:
        model = UserModel
        fields = GET_UNAUTHORIZED_FIELDS


class GetListUsersSerializer(serializers.ModelSerializer):
    @staticmethod
    def get(validated_data):
        return validated_data

    class Meta:
        model = UserModel
        fields = GET_UNAUTHORIZED_FIELDS


class RegistrationSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = UserModel(**validated_data)
        user.set_password(password)
        user.update_last_login()
        user.save()

        return user.data_for_me

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
        user.update_last_login()

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return user.data_for_me

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


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'name', 'email')
