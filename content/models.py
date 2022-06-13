from django.contrib.auth import get_user_model
from django.db import models
from django_softdelete.models import SoftDeleteModel
from model_utils.models import TimeStampedModel


class Post(SoftDeleteModel, TimeStampedModel, models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    image = models.ImageField(upload_to="post_images", blank=True)
    owner = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    to_post = models.ForeignKey(
        to="self", null=True, blank=True, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.owner.first_name + " Posted '" + self.title + "'"

    def get_reactions(self):
        return self.reaction_set.all()

    def get_comments(self):
        return Post.objects.filter(to_post=self.pk)

    @staticmethod
    def get_posts_only():
        return Post.objects.filter(to_post=None)


class Reaction(TimeStampedModel, models.Model):
    REACTION_TYPES = [
        (False, "DisLiked"),
        (True, "Liked"),
    ]
    reaction = models.BooleanField(choices=REACTION_TYPES)
    reacted_by = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    to_post = models.ForeignKey(to=Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "reacted_by",
            "to_post",
        )

    def get_reaction_name(self):
        return self.REACTION_TYPES[int(self.reaction)][1]

    def __str__(self) -> str:
        return (
            self.reacted_by.first_name
            + " "
            + self.get_reaction_name()
            + " '"
            + self.to_post.title
            + "' Post"
        )
