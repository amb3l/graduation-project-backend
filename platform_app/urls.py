from django.urls import path

from .views import CreateNewPlatformView, ListPlatformsView


urlpatterns = [
    path('', ListPlatformsView.as_view()),
    path('', CreateNewPlatformView.as_view()),
]
