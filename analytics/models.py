from django.contrib.auth.models import User
from django.db import models


class Country(models.Model):
    name: models.CharField = models.CharField(max_length=100, unique=True)
    code: models.CharField = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user: models.OneToOneField = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    country: models.ForeignKey = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, related_name="profiles"
    )

    def __str__(self):
        return self.user.username


class Blog(models.Model):
    title: models.CharField = models.CharField(max_length=200)
    content: models.TextField = models.TextField()
    author: models.ForeignKey = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blogs"
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # filters = {
    #     "and": {
    #         "author__username": "author",
    #         "author__profile__country__name": "country",
    #         "created_at": "date",
    #     }
    # }


class BlogView(models.Model):
    blog: models.ForeignKey = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name="views"
    )
    viewer: models.ForeignKey = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="viewed_blogs"
    )
    timestamp: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["timestamp"]),
        ]
