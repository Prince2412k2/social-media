import logging
from django.contrib.auth.backends import BaseBackend
from ..models import User, Credential
from .password_service import check_password, verify_password

logger = logging.getLogger(__name__)


class CredentialBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):  # pyright: ignore
        user = User.objects.get(email=email)
        is_valid = verify_password(user, password)
        if is_valid:
            logger.info(f"Validation Sucess : {user.id=} logged in")  # pyright: ignore
        else:
            logger.info("Validation Failed: wrong password")
        return user if is_valid else None

    def get_user(self, user_id: int):  # pyright: ignore
        try:
            logger.info("inside get_user method")
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            return None
