from typing import Optional, Type

from django.db import transaction
from core.models import Credential, User, Provider_Type
from core.services.password_service import PasswordService


class UserService:
    @staticmethod
    def get_user_by_email(email: str) -> User:
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise

    @staticmethod
    def get_user_by_pk(pk: int) -> User:
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise

    @staticmethod
    def update_password(pk: int | User, password: str):
        user = UserService.get_user_by_pk(pk) if isinstance(pk, int) else pk
        hashed = PasswordService.hash_password(password)
        if not user:
            return None
        user.password = hashed
        user.save()

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
                    "avatar": avatar,
                    "bio": bio,
                    "password": password,
                },
            )
            if provider:
                Credential.objects.update_or_create(
                    user=user, provider=provider, provider_id=provider_id
                )
        return user


class FollowService:
    @staticmethod
    def follow(self_user: User, user_to_follow_id: int):
        user_to_follow = UserService.get_user_by_pk(user_to_follow_id)
        self_user.follow(user_to_follow)

    @staticmethod
    def unfollow(self_user: User, user_to_unfollow_id: int):
        user_to_unfollow = UserService.get_user_by_pk(user_to_unfollow_id)
        self_user.unfollow(user_to_unfollow)

    @staticmethod
    def get_followers(self_user: User):
        return self_user.followers.all()

    @staticmethod
    def get_following(self_user: User):
        return self_user.following_users

    @staticmethod
    def remove_follower(self_user: User, user_to_unfollow_id: int):
        follower_to_remove = UserService.get_user_by_pk(user_to_unfollow_id)
        self_user.remove_follower(follower_to_remove)
