from deprecated import deprecated
from rest_framework.exceptions import AuthenticationFailed
from core.services.password_service import PasswordService
from core.models import User
from core.services.user_services import UserService


class PasswordAuthService:
    @staticmethod
    def login(email: str, password: str):
        if not password:
            raise AuthenticationFailed
        user = UserService.get_user_by_email(email)
        if not user:
            raise User.DoesNotExist
        if not PasswordService.verify_user_with_password(user, password):
            raise AuthenticationFailed("Invalid password")

        return user

    @staticmethod
    def signup(username: str, password: str, email: str):
        user = UserService.get_or_create(
            email=email, username=username, password=password
        )
        return user

    @staticmethod
    @deprecated(reason="Use TokenService.set_token_in_cookies with refresh=''")
    def logout():
        pass
