from abc import ABC, abstractmethod
from core.models import User


class BaseAuthService(ABC):
    @classmethod
    @abstractmethod
    def get_token_from_code(cls, code: str):
        """get auth token from code
        code is found in redirected url's query params"""
        ...

    @classmethod
    @abstractmethod
    def get_user_from_token(cls, id_token: str) -> User:
        """get user object from auth token provided by Credential.Providers"""
        ...
