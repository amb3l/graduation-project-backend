from django.urls import path

from .views import (
    UploadPassportAPIView,
    RegisterAPIView,
    LoginAPIView,

    GetUsersListAPIView,
    GetUserByIdAPIView,
    MeAPIView,
)

urlpatterns = [
    path('register', RegisterAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('users', GetUsersListAPIView.as_view(), name='user-list'),
    path('users/<int:id>', GetUserByIdAPIView.as_view(), name='user-detail'),
    path('me', MeAPIView.as_view(), name='user-me'),
    path(r'^users/(?P<passport_photo>[^/]+)$', UploadPassportAPIView.as_view(), name='confirm-passport'),
]
