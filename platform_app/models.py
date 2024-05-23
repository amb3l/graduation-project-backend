from django.db import models


class CoordinateModel(models.Model):
    x = models.FloatField()
    y = models.FloatField()

    objects = []

    def __str__(self):
        return f'{self.x} {self.y}'


class PlatformModel(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    coordinates = models.ManyToManyField(CoordinateModel)

    objects = []

    @property
    def full_address(self):
        return f'{self.city} {self.address}'

    def __str__(self):
        return f'{self.pk} | {self.name} | {self.full_address} | {self.coordinates}'
