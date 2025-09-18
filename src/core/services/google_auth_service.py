import requests
from rest_framework_simplejwt.exceptions import TokenError
from core.models import Credential
from social.settings import (
    GOOGLE_ACCESS_TOKEN_URL,
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_GET_USER_URL,
    GOOGLE_REDIRECT_URI,
)

from core.services.user_services import UserService


class GoogleAuthService:
    @staticmethod
    def get_token_from_code(code):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        body = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        res = requests.post(GOOGLE_ACCESS_TOKEN_URL, data=body, headers=headers)
        res.raise_for_status()
        return res.json().get("id_token")

    @staticmethod
    def custom_response(id_token):
        response = requests.get(GOOGLE_GET_USER_URL, params={"id_token": id_token})
        token_info = response.json()
        if response.status_code != 200 or token_info.get("aud") != GOOGLE_CLIENT_ID:
            raise TokenError
            return Response(
                {"error": "Invalid id_token"}, status=status.HTTP_400_BAD_REQUEST
            )
        sub = token_info.get("sub")
        email = token_info.get("email")
        username = email.split("@")[0]
        # TODO: try catch
        user = UserService.create_user(
            email, username, Credential.Provider.GOOGLE, provider_id=sub
        )
        # TODO: Work In Progress from here
        # Create JWT tokens
        refresh = RefreshToken.for_user(user)
        response = Response({"msg": "User loggedin"})
        response.set_cookie(
            "refresh_token",
            str(refresh),
            httponly=True,
            samesite="Lax",
            max_age=7 * 24 * 3600,  # 7 days
        )
        response.set_cookie(
            "access_token",
            str(refresh.access_token),
            httponly=True,
            samesite="Lax",
            max_age=15 * 60,  # 15 minutes
        )
        return response
