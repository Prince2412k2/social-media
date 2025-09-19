import logging
import requests
from rest_framework_simplejwt.exceptions import TokenError
from core.models import Credential, User
from social.settings import (
    GOOGLE_ACCESS_TOKEN_URL,
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_GET_USER_URL,
    GOOGLE_REDIRECT_URI,
)
from core.services.user_services import UserService
from core.services.base_auth_service import BaseAuthService

logger = logging.getLogger(__name__)


class GoogleAuthService(BaseAuthService):
    @classmethod
    def get_token_from_code(cls, code: str):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        body = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        res = requests.post(GOOGLE_ACCESS_TOKEN_URL, data=body, headers=headers)
        if not res.ok:
            logger.info(f"error while fetching token from {GOOGLE_ACCESS_TOKEN_URL=}")

        res.raise_for_status()
        return res.json().get("id_token")

    @classmethod
    def get_user_from_token(cls, id_token: str) -> User:
        response = requests.get(GOOGLE_GET_USER_URL, params={"id_token": id_token})
        token_info = response.json()
        if response.status_code != 200 or token_info.get("aud") != GOOGLE_CLIENT_ID:
            logger.info(f"error while fetching token from {GOOGLE_GET_USER_URL=}")
            raise TokenError
        logger.info(f"{token_info}")
        sub = token_info.get("sub")
        email = token_info.get("email")
        username = email.split("@")[0]
        avatar = token_info.get("picture")
        user = UserService.create_user(
            email, username, Credential.Provider.GOOGLE, avatar=avatar, provider_id=sub
        )
        return user
