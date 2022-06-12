from django_currentuser.middleware import get_current_authenticated_user
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Post
from .pagination import CustomPagination
from .serializers import PostSerializers


class PostList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.get_posts_only()
    pagination_class = CustomPagination
    serializer_class = PostSerializers


class PostCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.get_posts_only()
    serializer_class = PostSerializers

    def create(self, request, *args, **kwargs):
        request.data["owner"] = get_current_authenticated_user().pk
        return super().create(request, *args, **kwargs)


class PostSearch(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializers

    def get_queryset(self):
        title = self.request.query_params.get("title")
        body = self.request.query_params.get("body")
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")
        query = Post.get_posts_only()
        if title:
            query = query.filter(title__contains=title)
        if body:
            query = query.filter(body__contains=body)
        if first_name:
            query = query.filter(owner__first_name=first_name)
        if last_name:
            query = query.filter(owner__last_name=last_name)
        return query
