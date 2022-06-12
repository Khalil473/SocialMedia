from django.urls import path

from .views import PostCreate, PostList, PostSearch

urlpatterns = [
    path("", PostList.as_view(), name="PostsList"),
    path("search/", PostSearch.as_view(), name="search"),
    path("create/", PostCreate.as_view(), name="create"),
]
