from django.urls import path

from apps.review.views import ReviewCreateView

urlpatterns = [
    path('add_review', ReviewCreateView.as_view(), name='add-review'),
]
