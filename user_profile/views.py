from django_currentuser.middleware import get_current_authenticated_user
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile
from .serializers import ProfileSerializer


class MyProfile(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_current_user_profile(self):
        current_user = get_current_authenticated_user()
        if current_user is None:
            return None
        current_user_profile = Profile.objects.filter(user=current_user.pk)
        return current_user_profile.first()

    def patch(self, request):
        serializer = self.serializer_class(
            instance=self.get_current_user_profile(), data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        serializer = self.serializer_class(instance=self.get_current_user_profile())
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ProfileSearch(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_queryset(self):
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")
        location = self.request.query_params.get("location")
        email = self.request.query_params.get("email")
        query = Profile.objects.all()
        if first_name:
            query = query.filter(user__first_name=first_name)
        if last_name:
            query = query.filter(user__last_name=last_name)
        if location:
            query = query.filter(location=location)
        if email:
            query = query.filter(user__email=email)
        return query
