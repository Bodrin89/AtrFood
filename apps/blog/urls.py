from django.urls import path
from apps.blog.views import ListBlogsView

urlpatterns = [
    path('', ListBlogsView.as_view(), name='blogs-list'),
]
