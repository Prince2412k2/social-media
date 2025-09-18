from typing import Literal, Optional

from django.db import IntegrityError, transaction
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
    def update_password(pk: int | User, hashed_password: str):
        user = UserService.get_user_by_pk(pk) if isinstance(pk, int) else pk
        if not user:
            return None
        user.password = hashed_password
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
        provider: Provider_Type,
        password: Optional[str] = None,
        provider_id: Optional[str] = None,
    ) -> User:
        if password:
            return UserService._create_user_with_pass(email, username, password)
        with transaction.atomic():
            user, created = User.objects.get_or_create(
                email=email, defaults={"username": username}
            )
            Credential.objects.update_or_create(
                user=user, provider=provider, provider_id=provider_id
            )
        return user
