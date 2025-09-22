import logging
from typing import Optional, Tuple
import requests
from django.db import transaction
from storages.backends.s3 import mimetypes
from core.models import Credential, User, Provider_Type
from core.services.password_service import PasswordService
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)


class UserService:
    @staticmethod
    def get_user_by_email(email: str) -> User:
        return User.objects.get(email=email)

    @staticmethod
    def get_user_by_pk(pk: int) -> User:
        return User.objects.get(pk=pk)

    @staticmethod
    def update_password(pk: int | User, password: str):
        user = UserService.get_user_by_pk(pk) if isinstance(pk, int) else pk
        hashed = PasswordService.hash_password(password)
        user.password = hashed
        user.save()

    @staticmethod
    def resolve_avatar_url(content: str) -> Tuple[str, bytes]:
        res = requests.get(content, timeout=10)
        res.raise_for_status()
        content_type = res.headers.get("Content-Type")
        ext = (
            mimetypes.guess_extension(content_type.split(";")[0])
            if content_type
            else ""
        )
        file_name = f"profile{ext}"
        return file_name, res.content

    @staticmethod
    def save_avatar(
        user,
        filename: str,
        file_content: Optional[bytes] = None,
    ):
        if not user.pk:
            raise ValueError("User must be saved before uploading avatar")
        try:
            filename, file_content = (
                UserService.resolve_avatar_url(filename)
                if file_content is None
                else (filename, file_content)
            )
        except Exception as e:
            logger.info(
                f"Failed to save avatar file for {user.pk} to bucket | errors =>{e}"
            )
            return None
        logger.info(filename)
        ext = filename.split(".")[-1].lower()
        path = f"{user.pk}/profile.{ext}"
        if user.avatar:
            user.avatar.delete(save=False)
        user.avatar.save(path, ContentFile(file_content), save=True)
        logger.info(user.avatar)
        return path

    @staticmethod
    def _create_user_with_pass(
        email: str,
        username: str,
        password: str,
    ) -> User:
        user = User.objects.create(
            email=email,
            username=username,
            password=PasswordService.hash_password(password),
        )
        return user

    @staticmethod
    def create_user(
        email: str,
        username: str,
        provider: Optional[Provider_Type] = None,
        avatar: str = "",
        bio: str = "",
        password: Optional[str] = None,
        provider_id: Optional[str] = None,
    ) -> User:
        if password:
            return UserService._create_user_with_pass(email, username, password)
        with transaction.atomic():
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "username": username,
                    "bio": bio,
                    "password": password,
                },
            )
            # if avatar and created:
            UserService.save_avatar(user, avatar)
            if provider:
                Credential.objects.update_or_create(
                    user=user, provider=provider, provider_id=provider_id
                )
        return user


class FollowService:
    @staticmethod
    def follow(self_user: User, user_to_follow_id: int):
        user_to_follow = UserService.get_user_by_pk(user_to_follow_id)
        if user_to_follow == self_user:
            raise ValueError("Cannot follow yourself")
        self_user.following.add(user_to_follow)  # pyright: ignore

    @staticmethod
    def unfollow(self_user: User, user_to_unfollow_id: int):
        user_to_unfollow = UserService.get_user_by_pk(user_to_unfollow_id)
        if user_to_unfollow in self_user.following.all():  # type: ignore
            self_user.following.remove(user_to_unfollow)  # pyright: ignore
        else:
            raise ValueError("Can not unfollow a user you dont follow")

    @staticmethod
    def get_followers(self_user: User):
        return self_user.followers.all()

    @staticmethod
    def get_following(self_user: User):
        return self_user.following.all()  # pyright: ignore

    @staticmethod
    def remove_follower(self_user: User, user_to_unfollow_id: int):
        follower_to_remove = UserService.get_user_by_pk(user_to_unfollow_id)
        if follower_to_remove in self_user.followers.all():  # type: ignore
            self_user.followers.remove(
                follower_to_remove
            )  # removes the relationship in the join table
        else:
            raise ValueError(
                "Can not remove a User from followers who doesnt follow you"
            )
