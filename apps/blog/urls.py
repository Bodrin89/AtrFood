from django.urls import path
from apps.blog.views import ListBlogsView, GetBlogView

urlpatterns = [
    path('', ListBlogsView.as_view(), name='blogs-list'),
    path('<int:pk>', GetBlogView.as_view(), name='blog-retrieve'),
]
