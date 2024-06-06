from datetime import datetime

from rest_framework import serializers

from .models import OrderModel

from users.models import UserModel
from platform_app.models import PlatformModel

from users.serializers import UserSerializer
from platform_app.serializers import PlatformSerializer


class OrderStatusSerializer(serializers.ModelSerializer):
    status = serializers.CharField(max_length=10)

    CANCELED = OrderModel.STATUSES[OrderModel.CANCELED]
    RECEIVED = OrderModel.STATUSES[OrderModel.RECEIVED]

    def validate(self, data):
        if self.instance.status == self.CANCELED:
            raise serializers.ValidationError({"status": "The order status is already CANCELED"})

        if self.instance.status == self.RECEIVED:
            raise serializers.ValidationError({"status": "The order status is already RECEIVED"})

        return data

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)

        if instance.status == self.CANCELED:
            instance.date_canceled = datetime.now()

        if instance.status == self.RECEIVED:
            instance.date_received = datetime.now()

        instance.save()

        return instance

    class Meta:
        model = OrderModel
        fields = ['status', 'date_canceled', 'date_received']


class OrderSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    receiver = UserSerializer()

    sender_platform = PlatformSerializer()
    receiver_platform = PlatformSerializer()

    def to_internal_value(self, data):
        sender = UserModel.objects.get(id=data['sender_id'])
        receiver = UserModel.objects.get(id=data['receiver_id'])

        sender_platform = PlatformModel.objects.get(id=data['sender_platform_id'])
        receiver_platform = PlatformModel.objects.get(id=data['receiver_platform_id'])

        return {
            'sender': sender,
            'receiver': receiver,

            'sender_platform': sender_platform,
            'receiver_platform': receiver_platform,

            'delivery_cost': data['delivery_cost'],
            'payment_method': data['payment_method'],

            'date_created': datetime.now(),
            'date_canceled': None,
            'date_received': None,
        }

    def to_representation(self, instance):
        data = {
            'id': instance.id,
            'sender_id': instance.sender_id,
            'receiver_id': instance.receiver_id,
            'sender_platform_id': instance.sender_platform_id,
            'receiver_platform_id': instance.receiver_platform_id,

            'delivery_cost': instance.delivery_cost,
            'payment_method': instance.payment_method,

            'date_created': instance.date_created,
            'status': instance.status,
        }

        if instance.status == instance.STATUSES[instance.CANCELED]:
            data['date_canceled'] = instance.date_canceled

        if instance.status == instance.STATUSES[instance.RECEIVED]:
            data['date_received'] = instance.date_received

        return data

    def create(self, validation_data):
        return OrderModel.objects.create(**validation_data)

    class Meta:
        model = OrderModel
        fields = '__all__'
        read_only_fields = [
            'date_created',
            'date_canceled',
            'date_received',
        ]
