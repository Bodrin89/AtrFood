
from django.urls import path

from apps.payment.views import PaymentView, WebhookIoka

urlpatterns = [
    path('', PaymentView.as_view(), name='post-payment'),
    path('webhook/payment/3jhghj7fg6d3', WebhookIoka.as_view(), name='post-payment'),
]