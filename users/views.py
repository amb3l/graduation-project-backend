import jwt

from django.conf import settings
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from .models import UserModel
from .serializers import (
    RegistrationSerializer,
    LoginSerializer,
    MeSerializer,

    GetListUsersSerializer,
    GetUserByIdSerializer,
)


class GetUserByIdAPIView(APIView):
    serializer_class = GetUserByIdSerializer
    queryset = UserModel.objects.all()
    permission_classes = (AllowAny,)

    def get(self, _, id):
        serializer = self.serializer_class(
            self.queryset.get(id=id)
        )

        return Response(
            serializer.data,
            status=HTTP_200_OK,
        )


class GetUsersListAPIView(APIView):
    serializer_class = GetListUsersSerializer
    queryset = UserModel.objects.all()
    permission_classes = (AllowAny,)

    def get(self, _):
        serializer = self.serializer_class(
            self.queryset.all(),
            many=True,
        )

        return Response(
            serializer.data,
            status=HTTP_200_OK,
        )
from .serializers import RegistrationSerializer, LoginSerializer, MeSerializer


class RegisterAPIView(APIView):
    serializer_class = RegistrationSerializer
    queryset = UserModel.objects.all()
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
        }

        refresh_token = RefreshToken.for_user(user)
        refresh_token.payload.update(user_data)

        access_token = AccessToken.for_user(user)
        access_token.payload.update(user_data)

        return Response({
            'me': user_data,
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

        user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
        }

        refresh_token = RefreshToken.for_user(user)
        refresh_token.payload.update(user_data)

        access_token = AccessToken.for_user(user)
        access_token.payload.update(user_data)

        return Response({
            'me': user_data,
            'refresh': str(refresh_token),
            'access': str(access_token),
        }, status=HTTP_200_OK)


class MeAPIView(APIView):
    serializer_class = MeSerializer
    queryset = UserModel.objects.all()
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        auth_header = request.headers['Authorization']
        access_token = auth_header.split()[1]
        user = jwt.decode(jwt=access_token, key=settings.SECRET_KEY, algorithms=['HS256'])

        serializer = MeSerializer(user)

        return Response(serializer.data)

