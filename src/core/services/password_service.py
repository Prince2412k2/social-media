import logging
from django.contrib.auth.hashers import make_password, check_password

from core.models import User
from core.services.user_services import UserService

logger = logging.getLogger(__name__)


class PasswordService:
    @staticmethod
    def hash_password(password: str) -> str:
        return make_password(password)

    @staticmethod
    def update_password(user, raw_password):
        """hashes and upades password for given user in database"""
        hashed = make_password(raw_password)
        UserService.update_password(user, hashed)
        logger.info(f"Credential updated for {user.id=}")

    @staticmethod
    def verify_user_with_password(user, raw_password):
        """validates db user to given password"""
        hashed = user.password
        return check_password(raw_password, hashed)
