from django.db.models import Model, CharField
from django.contrib.gis.db.models import PointField


class PlatformModel(Model):
    name = CharField(max_length=50)
    city = CharField(max_length=100)
    address = CharField(max_length=100)
    coordinates = PointField()

    @property
    def full_address(self):
        return "%s %s" % (self.city, self.address)

