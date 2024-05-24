from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from .models import UserModel
from .serializers import RegistrationSerializer, LoginSerializer


class RegisterAPIView(APIView):
    serializer_class = RegistrationSerializer
    queryset = UserModel.objects.all()
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        payload = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
        }

        refresh_token = RefreshToken.for_user(user)
        refresh_token.payload.update(payload)

        access_token = AccessToken.for_user(user)
        access_token.payload.update(payload)

        return Response({
            'refresh': str(refresh_token),
            'access': str(access_token),
        }, status=HTTP_201_CREATED)


class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    queryset = UserModel.objects.all()
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        data = request.data
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None or password is None:
            return Response({
                'error': 'Both email and password are required!',
            }, status=HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)

        if user is None:
            return Response({
                'error': 'Incorrect credentials!'
            }, status=HTTP_401_UNAUTHORIZED)

        payload = {
            'id': user.id,
            'email': user.email,
        }

        refresh_token = RefreshToken.for_user(user)
        refresh_token.payload.update(payload)

        access_token = AccessToken.for_user(user)
        access_token.payload.update(payload)

        return Response({
            'refresh': str(refresh_token),
            'access': str(access_token),
        }, status=HTTP_200_OK)
