from rest_framework.views import APIView
from rest_framework.response import Response

from .models import UserModel
from .serializers import UserSerializer


class RegisterView(APIView):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()

    @staticmethod
    def post(request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
