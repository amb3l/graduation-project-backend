from django.urls import path

from .views import PlatformAPIView


urlpatterns = [
    path('', PlatformAPIView.as_view()),
]
