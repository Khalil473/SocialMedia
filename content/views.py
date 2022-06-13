from django_currentuser.middleware import get_current_authenticated_user
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, Reaction
from .pagination import CustomPagination
from .serializers import PostSerializers, ReactionsSerializer


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
        # so a user can't update others posts
        query = get_current_authenticated_user().post_set.all()
        return query


class PostDelete(APIView):
    def delete(self, request, pk):
        p: Post = None
        try:
            # so a user can't delete others posts
            p = get_current_authenticated_user().post_set.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        p.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        query = get_current_authenticated_user().post_set.filter(to_post=None)
        return query


class PostComments(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        post = None
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializers(post.get_comments(), many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PostReact(APIView):
    permission_classes = [IsAuthenticated]

    def get_reaction(self, request):
        current_user = get_current_authenticated_user()
        to_post = request.data.get("to_post", None)
        if not to_post:
            return None
        try:
            return current_user.reaction_set.get(to_post=to_post)
        except Reaction.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        _mutable = request.data._mutable
        request.data._mutable = True
        request.data["reacted_by"] = get_current_authenticated_user().pk
        request.data._mutable = _mutable

        serializer = ReactionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        reaction = self.get_reaction(request)
        if not reaction:
            return Response(status=status.HTTP_404_NOT_FOUND)

        reaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request):
        reaction = self.get_reaction(request)
        if not reaction:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ReactionsSerializer(
            instance=reaction, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        reaction = self.get_reaction(request)
        if not reaction:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ReactionsSerializer(instance=reaction)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
