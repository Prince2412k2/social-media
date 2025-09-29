from typing import Any, Optional
from social.settings import SIMPLE_JWT, DEBUG
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from core.models import User
from core.services.user_services import UserService


class TokenService:
    @staticmethod
    def set_token_in_cookies(
        refresh: Optional[RefreshToken], response: Response
    ) -> Response:
        """
        sets access_token and refreshtokens in httponly cookie
        if refresh=None it will remove both token entries from cookie
        if refresh=RefreshToken it will replace old refresh_token and access_token with new
        """
        if not refresh:
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")
            return response
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)
        response.set_cookie(
            "access_token",
            access_token,
            httponly=True,
            samesite="Lax",
            secure=not DEBUG,
            max_age=SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds(),
            path="/",
        )
        response.set_cookie(
            "refresh_token",
            refresh_token,
            httponly=True,
            samesite="Lax",
            secure=not DEBUG,
            max_age=SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds(),
            path="/",
        )
        return response

    @staticmethod
    def get_refresh_token_for_user(user: User):
        return RefreshToken.for_user(user)

    @staticmethod
    def validate_refresh_token(refresh: Any):
        try:
            return RefreshToken(refresh)
        except TokenError:
            raise

    @staticmethod
    def renew_refresh_token(old_refresh_token: Any) -> RefreshToken:
        if not old_refresh_token:
            raise ValueError()
        refresh = TokenService.validate_refresh_token(old_refresh_token)
        pk = refresh.access_token.get("user_id")
        user = UserService.get_user_by_pk(pk)

        new_refresh = TokenService.get_refresh_token_for_user(user)
        return new_refresh
