from django.urls import path

from .views import RegisterAPIView, LoginAPIView, GetUsersListView


urlpatterns = [
    path('register', RegisterAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('users', GetUsersListView.as_view()),
]
