import logging
from django.contrib.auth.hashers import make_password, check_password

logger = logging.getLogger(__name__)


class PasswordService:
    @staticmethod
    def hash_password(password: str) -> str:
        return make_password(password)

    @staticmethod
    def verify_user_with_password(user, raw_password):
        """validates db user to given password"""
        hashed = user.password
        is_valid = check_password(raw_password, hashed)
        return is_valid
