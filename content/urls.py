from django.urls import path

from .views import MyPosts, PostCreate, PostList, PostSearch

urlpatterns = [
    path("", PostList.as_view(), name="PostsList"),
    path("search/", PostSearch.as_view(), name="search"),
    path("create/", PostCreate.as_view(), name="create"),
    path("my_posts/", MyPosts.as_view(), name="my_posts"),
]
