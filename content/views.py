from django_currentuser.middleware import get_current_authenticated_user
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post
from .pagination import CustomPagination
from .serializers import PostSerializers


class PostCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.get_posts_only()
    serializer_class = PostSerializers

    def create(self, request, *args, **kwargs):
        _mutable = request.data._mutable
        request.data._mutable = True
        request.data["owner"] = get_current_authenticated_user().pk
        request.data._mutable = _mutable
        return super().create(request, *args, **kwargs)


class PostUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializers

    def get_queryset(self):
        query = get_current_authenticated_user().post_set.all()
        return query


class PostDelete(APIView):
    def delete(self, request, pk):
        p: Post = None
        try:
            p = get_current_authenticated_user().post_set.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        p.delete()
        return Response(status=status.HTTP_200_OK)


class PostSearch(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializers
    pagination_class = CustomPagination

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


class MyPosts(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializers
    pagination_class = CustomPagination

    def get_queryset(self):
        query = get_current_authenticated_user().post_set.all()
        return query
