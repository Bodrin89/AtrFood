
from django.urls import path

from apps.payment.views import PaymentView

urlpatterns = [
    path('', PaymentView.as_view(), name='post-payment'),
]