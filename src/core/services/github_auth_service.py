import logging
from typing import List
import requests
from rest_framework_simplejwt.exceptions import TokenError
from core.models import Credential, User
from social.settings import (
    GITHUB_CLIENT_ID,
    GITHUB_CLIENT_SECRET,
    GITHUB_ACCESS_TOKEN_URL,
    GITHUB_GET_USER_URL,
    GITHUB_EMAIL_URL,
)

from core.services.user_services import UserService
from core.services.base_auth_service import BaseAuthService

logger = logging.getLogger(__name__)


class GihubAuthService(BaseAuthService):
    @classmethod
    def get_token_from_code(cls, code: str):
        headers = {"Accept": "application/json"}
        body = {
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
        }
        res = requests.post(GITHUB_ACCESS_TOKEN_URL, data=body, headers=headers)
        if not res.ok:
            logger.info(f"error while fetching token from {GITHUB_ACCESS_TOKEN_URL=}")

        res.raise_for_status()
        return res.json().get("access_token")

    @classmethod
    def get_user_from_token(cls, id_token: str) -> User:
        headers = {"Authorization": f"token {id_token}"}
        response = requests.get(GITHUB_GET_USER_URL, headers=headers)
        if not response.ok:
            logger.info(f"error while fetching token from {GITHUB_GET_USER_URL=}")
            raise TokenError
        token_info = response.json()
        sub = token_info.get("sub")
        email = GihubAuthService.get_email_helper(id_token)
        username = token_info.get("login")
        avatar = token_info.get("avatar_url")
        user = UserService.get_or_create(
            email, username, Credential.Provider.GITHUB, provider_id=sub, avatar=avatar
        )
        return user

    @classmethod
    def get_email_helper(cls, id_token: str):
        headers = {"Authorization": f"token {id_token}"}
        response = requests.get(GITHUB_EMAIL_URL, headers=headers)
        if not response.ok:
            return ""
        responses: List = response.json()
        primary_email = next((x["email"] for x in responses if x.get("primary")), "")
        return primary_email
