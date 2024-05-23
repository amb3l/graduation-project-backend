from django.db import models


class PlatformModel(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    x = models.FloatField()
    y = models.FloatField()
    objects = []

    @property
    def full_address(self):
        return f'{self.city} {self.address}'

    @property
    def coordinates(self):
        return f'{self.x} {self.y}'

    def __str__(self):
        return f'{self.pk} | {self.name} | {self.full_address} | {self.coordinates}'
