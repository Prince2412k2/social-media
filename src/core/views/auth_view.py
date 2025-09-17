import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from dj_rest_auth.views import LoginView
from core.auth.password_service import verify_password
from core.models import Credential, User
import requests
from django.db import transaction

from social.settings import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, SIMPLE_JWT
from social.settings import GOOGLE_CLIENT_ID


logger = logging.getLogger(__name__)


class CookieLoginView(LoginView):
    def post(self, request):
        try:
            user = User.objects.get(email=request.data.get("email"))
        except User.DoesNotExist:
            return Response(
                {"ERROR": "USER DOESN'T EXIST"}, status.HTTP_400_BAD_REQUEST
            )
        if not verify_password(user, request.data.get("password")):
            return Response({"ERROR": "WRONG PASSWORD"}, status.HTTP_400_BAD_REQUEST)
        self.user = user

        refresh = RefreshToken.for_user(self.user)  # pyright: ignore

        response = Response({"msg": "Logged In"})

        response.set_cookie(
            "access_token",
            str(refresh.access_token),
            httponly=True,
            samesite="Lax",
            secure=False,
            max_age=SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds(),
        )
        response.set_cookie(
            "refresh_token",
            str(refresh),
            httponly=True,
            samesite="Lax",
            secure=False,
            max_age=SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds(),
        )
        return response


class CookieTokenRefreshView(APIView):
    def get(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response(
                {"detail": "No refresh token"}, status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            refresh = RefreshToken(refresh_token)
        except Exception:
            return Response(
                {"detail": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED
            )
        user = User.objects.get(pk=refresh.access_token.get("user_id"))
        # Rotate refresh token
        new_refresh = RefreshToken.for_user(user)
        logger.info(new_refresh)

        response = Response()
        # Set new refresh token in cookie
        response.set_cookie(
            "refresh_token", str(new_refresh), httponly=True, samesite="Lax"
        )
        return response


class LogoutView(APIView):
    def get(self, request):
        response = Response({"msg": "Logged out"})
        response.set_cookie(
            "refresh_token",
            "",
            httponly=True,
            samesite="Lax",
            max_age=0,
        )

        response.set_cookie(
            "access_token",
            "",
            httponly=True,
            samesite="Lax",
            max_age=0,
        )
        return response


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

    def post(self, request):
        id_token = request.data.get("id_token")
        logger.info(f"{id_token=}")
        if not id_token:
            return Response(
                {"error": "id_token required"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Verify token with Google
        response = requests.get(
            "https://oauth2.googleapis.com/tokeninfo", params={"id_token": id_token}
        )
        token_info = response.json()
        logger.info(f"{token_info=}")
        if response.status_code != 200 or token_info.get("aud") != GOOGLE_CLIENT_ID:
            return Response(
                {"error": "Invalid id_token"}, status=status.HTTP_400_BAD_REQUEST
            )
        sub = token_info.get("sub")
        email = token_info.get("email")

        with transaction.atomic():
            user, _ = User.objects.get_or_create(
                email=email, defaults={"username": email.split("@")[0]}
            )
            Credential.objects.update_or_create(
                user=user, provider=Credential.Provider.GOOGLE, provider_id=sub
            )

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


class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter

    def get_token_from_query(self, query):
        headers = {"Accept": "application/json"}
        body = {
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": query,
        }
        res = requests.post(
            "https://github.com/login/oauth/access_token", headers=headers, data=body
        ).json()
        return res["access_token"]

    def get_user_from_token(self, token):
        headers = {"Authorization": f"token {token}"}
        return requests.get("https://api.github.com/user", headers=headers).json()

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

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {"email": user.email, "username": user.username},
            }
        )
