from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


from .models import PlatformModel
from .serializers import PlatformSerializer


class CreateNewPlatformView(APIView):
    serializer_class = PlatformSerializer
    queryset = PlatformModel.objects.all()
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        serializer = PlatformSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class ListPlatformsView(APIView):
    serializer_class = PlatformSerializer
    queryset = PlatformModel.objects.all()
    permission_classes = (AllowAny,)

    def get(self, _):
        serializer = PlatformSerializer(self.queryset.all(), many=True)
        return Response(serializer.data)
