from django.db import models


class OrderModel(models.Model):
    number = models.CharField(max_length=20)

    sender = models.ForeignKey('UserModel', on_delete=models.CASCADE)
    receiver = models.ForeignKey('UserModel', on_delete=models.CASCADE)

    sender_platform = models.ForeignKey('PlatformModel', on_delete=models.CASCADE)
    receiver_platform = models.ForeignKey('PlatformModel', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.number}'
