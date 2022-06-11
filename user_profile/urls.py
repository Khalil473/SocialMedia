from django.urls import path

from .views import MyProfile, ProfileSearch

urlpatterns = [
    # path("all/", ProfileList.as_view(), name="all"),
    path("my_profile/", MyProfile.as_view(), name="my_profile"),
    path("search/", ProfileSearch.as_view(), name="search"),
]
