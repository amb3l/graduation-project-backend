from django.conf import settings
from django.db import models
from django.utils import timezone


def upload_to(_, filename):
    return 'passport_photos/{filename}'.format(filename=filename)


class PassportPhotoModel(models.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _file_manager = settings.FILE_MANAGER.init_user(
            name='Passports',
            folder='passport_photos',
        )

    title = models.CharField(max_length=80, blank=False, null=False)
    description = models.TextField()

    date_uploaded = models.DateTimeField(timezone.now())
    url = models.ImageField(upload_to=upload_to, blank=True, null=True)

    objects = []
