from django.urls import path

from .views import (
    OrderAPIView,
    OrderCanceledAPIView,
    OrderReceivedAPIView,
)

urlpatterns = [
    path('', OrderAPIView.as_view(), name='orders'),
    path('<int:id>/cancel', OrderCanceledAPIView.as_view(), name='cancel-order'),
    path('<int:id>/receive', OrderReceivedAPIView.as_view(), name='set-order-received'),
]
