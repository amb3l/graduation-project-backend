from django.urls import path

from .views import CreateNewPlatformView, ListPlatformsView


urlpatterns = [
    path('', ListPlatformsView.as_view()),
    path('create', CreateNewPlatformView.as_view()),
]
