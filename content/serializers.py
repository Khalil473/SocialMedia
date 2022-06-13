from rest_framework import serializers

from .models import Post, Reaction


class PostSerializers(serializers.ModelSerializer):
    owner_email = serializers.CharField(source="owner.email", required=False)

    class Meta:
        model = Post
        fields = (
            "pk",
            "title",
            "body",
            "image",
            "created",
            "modified",
            "owner_email",
            "owner",
            "to_post",
        )


class ReactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ("reaction", "to_post", "reacted_by")
