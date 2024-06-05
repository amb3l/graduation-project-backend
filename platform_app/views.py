from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.status import (
    HTTP_200_OK,
)


from .models import PlatformModel
from .serializers import PlatformSerializer


class PlatformAPIView(APIView):
    serializer_class = PlatformSerializer
    queryset = PlatformModel.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, _):
        serializer = self.serializer_class(self.queryset.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=HTTP_200_OK,
        )
