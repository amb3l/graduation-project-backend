from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import UserSerializer


class RegisterView(APIView):
    @staticmethod
    def post(request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
