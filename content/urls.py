from django.urls import path

from .views import (
    MyPosts,
    PostComments,
    PostCreate,
    PostDelete,
    PostReact,
    PostSearch,
    PostUpdate,
)

urlpatterns = [
    path("search/", PostSearch.as_view(), name="search"),
    path("create/", PostCreate.as_view(), name="create"),
    path("my_posts/", MyPosts.as_view(), name="my_posts"),
    path("update/<int:pk>/", PostUpdate.as_view(), name="update"),
    path("delete/<int:pk>/", PostDelete.as_view(), name="delete"),
    path("comments/<int:pk>/", PostComments.as_view(), name="comments"),
    path("react/", PostReact.as_view(), name="react"),
]
