from django.db import models


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


class User(BaseModel):
    """
    User model for database
    """

    username = models.CharField(max_length=100)
    email = models.EmailField(
        unique=True,
    )
    bio = models.TextField(blank=True)
    avatar = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} with email {self.email}"


class Credential(BaseModel):
    """
    Credential model for users
    """

    class Provider(models.TextChoices):
        PASSWORD = "password", "Passwod"
        GOOGLE = "google", "Google"
        GITHUB = "github", "GitHub"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="credentials")
    provider = models.CharField(max_length=20, choices=Provider.choices)
    provider_id = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:  # pyright: ignore
        unique_together = ("provider", "provider_id")

    def __str__(self):
        return f"{self.provider} for {self.user}"
