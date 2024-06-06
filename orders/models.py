from django.db import models

from users.models import UserModel
from platform_app.models import PlatformModel


class OrderModel(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)

    sender = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='receiver')

    sender_platform = models.ForeignKey(PlatformModel, on_delete=models.CASCADE, related_name='sender_platform')
    receiver_platform = models.ForeignKey(PlatformModel, on_delete=models.CASCADE, related_name='receiver_platform')

    delivery_cost = models.FloatField()
    payment_method = models.CharField(max_length=25)

    ACTIVE = 'ACTIVE'
    CANCELED = 'CANCELED'
    RECEIVED = 'RECEIVED'

    STATUSES = {
        ACTIVE: 'Активный',
        CANCELED: 'Отменён',
        RECEIVED: 'Доставлен',
    }

    status = models.CharField(max_length=10, choices=STATUSES, default=STATUSES[ACTIVE])

    date_created = models.DateTimeField(null=True)
    date_canceled = models.DateTimeField(null=True)
    date_received = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.pk} | {self.status}'
