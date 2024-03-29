from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.utils.translation import gettext_lazy as _
from apps.order.models import OrderItem
from apps.review.models import ReviewProductModel
from apps.review.serializers import ReviewCreateSerializer


class ReviewProductViewSet(ModelViewSet):
    """Просмотр всех отзывов и создание отзывов с проверкой на покупку товара"""
    serializer_class = ReviewCreateSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        return ReviewProductModel.objects.all().filter(moderation=True)

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), ]
        return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        user = request.user
        product = request.data.get('product')

        if not OrderItem.objects.filter(order__user=user, product=product).exists():
            return Response({'error': _('Вы не можете оставить отзыв на этот товар, так как не совершали его покупку.')},
                            status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def reviews_for_product(self, request, pk=None):
        if pk is None:
            return Response(
                {'error': _('Необходимо указать ID продукта.')},
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = self.get_queryset().filter(product=pk)
        if queryset:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return Response(
            {'detail': _('Комментарии по данному продукту отсутствуют')},
            status=status.HTTP_204_NO_CONTENT
        )
