from django.db.models import Q
from django.db.models import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,

    HTTP_404_NOT_FOUND,
)

from .models import OrderModel
from .serializers import OrderSerializer, OrderStatusSerializer


class OrderCanceledAPIView(APIView):
    serializer_class = OrderStatusSerializer
    queryset = OrderModel.objects.all()
    permission_classes = (IsAuthenticated,)

    CANCELED = OrderModel.STATUSES[OrderModel.CANCELED]

    def patch(self, _, id):
        me = self.request.user
        allowed_queryset = self.queryset.filter(Q(sender=me) | Q(receiver=me))
        try:
            order = allowed_queryset.get(id=id)
        except ObjectDoesNotExist:
            return Response(
                {"error": "Either the order has not found or is unavailable!"},
                status=HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(instance=order, data={"status": self.CANCELED}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": f"The order #{order.id} status has been successfully changed to CANCELED"},
            status=HTTP_200_OK,
        )


class OrderReceivedAPIView(APIView):
    serializer_class = OrderStatusSerializer
    queryset = OrderModel.objects.all()
    permission_classes = (IsAuthenticated,)

    RECEIVED = OrderModel.STATUSES[OrderModel.RECEIVED]

    def patch(self, _, id):
        me = self.request.user
        allowed_queryset = self.queryset.filter(Q(receiver=me))
        try:
            order = allowed_queryset.get(id=id)
        except ObjectDoesNotExist:
            return Response(
                {"error": "Either the order has not found or is unavailable!"},
                status=HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(instance=order, data={"status": self.RECEIVED}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": f"The order #{order.id} status has been successfully changed to RECEIVED"},
            status=HTTP_200_OK,
        )


class OrderAPIView(APIView):
    serializer_class = OrderSerializer
    queryset = OrderModel.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, _):
        me = self.request.user
        allowed_queryset = self.queryset.filter(Q(sender=me) | Q(receiver=me))
        serializer = self.serializer_class(allowed_queryset.all(), many=True)

        return Response(
            data=serializer.data,
            status=HTTP_200_OK,
        )

    def post(self, request):
        me = request.user
        serializer = self.serializer_class(data={**request.data, "sender_id": me.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=HTTP_201_CREATED,
        )
