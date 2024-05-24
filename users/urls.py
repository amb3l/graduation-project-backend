from django.urls import path

from .views import RegisterAPIView, LoginAPIView, MeAPIView


urlpatterns = [
    path('register', RegisterAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('me', MeAPIView.as_view()),
]
