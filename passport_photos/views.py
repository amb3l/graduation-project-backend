from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser

from .models import PassportPhotoModel
from .serializers import PassportPhotoSerializer


class PassportPhotoViewSet(viewsets.ModelViewSet):
    queryset = PassportPhotoModel.objects.order_by('-creation_date')
    serializer_class = PassportPhotoSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()
