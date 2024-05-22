from django.db import models


class PlatformModel(models.Model):
    name = models.CharField()
    city = models.CharField()
    address = models.CharField()

    @property
    def full_address(self):
        return "%s %s" % (self.city, self.address)

