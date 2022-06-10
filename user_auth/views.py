from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSignInSerializer, UserSignUpSerializer


class SignInAPIView(APIView):
    def post(self, request):
        serializer = UserSignInSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUpAPIView(APIView):
    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.validated_data, status=status.HTTP_201_CREATED
            )
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):  # for testing
        demoData = {
            "password": "12ads34kyle",
            "first_name": "aaa",
            "last_name": "aaa",
            "email": "aaa33@aaa.com",
        }
        return Response(data=demoData, status=status.HTTP_200_OK)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
