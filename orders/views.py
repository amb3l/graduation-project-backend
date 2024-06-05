from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
)

from .models import OrderModel
from .serializers import OrderSerializer


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
