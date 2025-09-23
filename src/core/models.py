import logging
from typing import Literal
from boto3.s3.transfer import TransferConfig
from django.contrib.auth.models import AbstractUser
from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

logger = logging.getLogger(__name__)
user_stroage = S3Boto3Storage(**settings.STORAGES["users"]["OPTIONS"])
post_storage = S3Boto3Storage(**settings.STORAGES["posts"]["OPTIONS"])
config = TransferConfig(multipart_threshold=30 * 1024 * 1024)


class BaseManager(models.Manager):
    """
    BaseManager to override default models.Manager behaviour
    here adding filter to only show entries with is_deleted=False
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class BaseModel(models.Model):
    """
    BaseModel to override default models.Model behaviour
    here adding soft delete for delete() method
    """

    is_deleted = models.BooleanField(default=False)
    objects = BaseManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):  # pyright: ignore
        self.is_deleted = True
        self.save(using=using)


class User(BaseModel, AbstractUser):  # pyright: ignore
    """
    User model for database
    """

    username = models.CharField(max_length=100)
    password = models.CharField(max_length=128, blank=True, null=True)
    email = models.EmailField(
        unique=True,
    )
    bio = models.TextField(blank=True)
    avatar = models.ImageField(
        blank=True,
        null=True,
        storage=user_stroage,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="following"
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"user({self.pk})"

    def __repr__(self):
        return f"{self.username} with email {self.email}"

    def user_profile_path(self, filename):
        ext = filename.split(".")[-1]
        return f"{self.id}/profile.{ext}"  # pyright: ignore User doesnt know its id yet

    def delete(self, using=None, keep_parents=False):  # pyright: ignore
        self.is_deleted = True
        self.followers.clear()
        self.following.clear()  # pyright: ignore
        self.save(using=using)


class Credential(BaseModel):
    """
    Credential model for users
    """

    class Provider(models.TextChoices):
        GOOGLE = "google", "Google"
        GITHUB = "github", "GitHub"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="credentials")
    provider = models.CharField(max_length=255, choices=Provider.choices)
    provider_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:  # pyright: ignore
        unique_together = ("provider", "provider_id")

    def __str__(self):
        return f"{self.provider} for {self.user}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    image = models.ImageField(blank=True, null=True, storage=post_storage)
    caption = models.TextField()
    liked_by = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"post({self.pk}) by {self.user}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]


Provider_Type = Literal[Credential.Provider.GOOGLE, Credential.Provider.GITHUB]
