from django.db import models


class PlatformModel(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    x = models.FloatField()
    y = models.FloatField()

    @property
    def full_address(self):
        return "%s %s" % (self.city, self.address)

