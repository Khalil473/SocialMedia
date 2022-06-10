from django.urls import path

from .views import SignInAPIView, SignUpAPIView

urlpatterns = [
    path("sign_up/", SignUpAPIView.as_view(), name="sign_up"),
    path("log_in/", SignInAPIView.as_view(), name="log_in"),
]
