from datetime import datetime

from django.db import models


class OrderModel(models.Model):
    sender = models.ForeignKey('UserModel', on_delete=models.CASCADE)
    receiver = models.ForeignKey('UserModel', on_delete=models.CASCADE)

    sender_platform = models.ForeignKey('PlatformModel', on_delete=models.CASCADE)
    receiver_platform = models.ForeignKey('PlatformModel', on_delete=models.CASCADE)

    delivery_cost = models.FloatField()
    payment_method = models.CharField(max_length=25)

    STATUSES = models.Choices(
        ('ACTIVE', 'Активный'),
        ('CANCELED', 'Отменён'),
        ('RECEIVED', 'Доставлен'),
    )

    status = models.CharField(max_length=10, choices=STATUSES)

    date_created = models.DateTimeField(default=datetime.now())
    date_canceled = models.DateTimeField()
    date_received = models.DateTimeField()

    def __str__(self):
        return f'{self.pk}'
