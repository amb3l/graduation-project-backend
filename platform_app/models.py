import json

from django.db import models


class PlatformModel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    coordinates = models.CharField(max_length=100, unique=True)

    @property
    def full_address(self):
        return f'{self.city} {self.address}'

    def set_coordinates(self, value):
        self.coordinates = json.dumps(value)

    def get_constraints(self):
        return json.loads(self.coordinates)

    def __str__(self):
        return f'{self.pk} | {self.name} | {self.full_address} | {self.coordinates}'
