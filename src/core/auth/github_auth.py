import logging
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from core.models import Credential, User
import requests
from django.db import transaction

from social.settings import (
    GITHUB_CLIENT_ID,
    GITHUB_CLIENT_SECRET,
    GITHUB_ACCESS_TOKEN_URL,
    GITHUB_GET_USER_URL,
)


logger = logging.getLogger(__name__)


class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter

    def get_token_from_query(self, query):
        headers = {"Accept": "application/json"}
        body = {
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": query,
        }
        res = requests.post(GITHUB_ACCESS_TOKEN_URL, headers=headers, data=body).json()
        return res["access_token"]

    def get_user_from_token(self, token):
        headers = {"Authorization": f"token {token}"}
        return requests.get(GITHUB_GET_USER_URL, headers=headers).json()

    def get(self, request):
        query = request.query_params.get("code", False)
        if not query:
            return Response(
                {"error": "No 'code' field fount in query"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        token = self.get_token_from_query(query)
        github_user = self.get_user_from_token(token)
        return self.custom_response(github_user)

    def post(self, request, *args, **kwargs):
        access_token = request.data.get("access_token")

        github_user = self.get_user_from_token(access_token)
        if not github_user:
            return Response(
                {"error": "access_token required or code"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return self.custom_response(github_user)

    def custom_response(self, github_user):
        github_id = github_user.get("id")
        email = github_user.get("email") or f"github_{github_id}@example.com"
        username = github_user.get("login") or email.split("@")[0]
        logger.info(f"{github_id=}")
        if not github_id:
            return Response(
                {"error": "Invalid access_token"}, status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            user, _ = User.objects.get_or_create(
                email=email, defaults={"username": username}
            )
            Credential.objects.update_or_create(
                user=user,
                provider=Credential.Provider.GITHUB,
                provider_id=str(github_id),
            )

        response = Response({"msg": "User loggedin"})

        refresh = RefreshToken.for_user(user)
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
