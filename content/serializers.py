from rest_framework import serializers

from .models import Post, Reaction


class PostSerializers(serializers.ModelSerializer):
    owner_email = serializers.CharField(source="owner.email", required=False)

    class Meta:
        model = Post
        fields = (
            "title",
            "body",
            "image",
            "created",
            "modified",
            "owner_email",
            "owner",
        )

    def get_validation_exclusions(self):
        exclusions = super().get_validation_exclusions()
        return exclusions + ["owner"]
