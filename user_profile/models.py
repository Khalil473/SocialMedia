from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(
        to=get_user_model(), on_delete=models.CASCADE, null=False
    )
    bio = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=50, null=True)
    image = models.ImageField(upload_to="user_images", default="default.png")

    def __str__(self) -> str:
        return str(self.user) + _(" profile")
