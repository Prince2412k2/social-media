from enum import unique
import logging
from typing import Literal
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models

logger = logging.getLogger(__name__)


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
    avatar = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="following"
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.username} with email {self.email}"

    @property
    def following_users(self) -> models.QuerySet["User"]:
        return self.following.all()  # pyright: ignore

    def follow(self, user: "User"):
        if user == self:
            raise ValueError("Cannot follow yourself")
        self.following.add(user)  # pyright: ignore

    def unfollow(self, user: "User"):
        if user in self.following.all():  # type: ignore
            self.following.remove(user)  # pyright: ignore

    def remove_follower(self, user: "User"):
        if user in self.followers.all():  # type: ignore
            self.followers.remove(user)  # removes the relationship in the join table

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


Provider_Type = Literal[Credential.Provider.GOOGLE, Credential.Provider.GITHUB]
