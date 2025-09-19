import logging
from dj_rest_auth.registration.views import RegisterView
from django.db import IntegrityError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError
from dj_rest_auth.views import LoginView
from core.models import User
from core.services.password_auth_service import PasswordAuthService
from core.services.token_service import TokenService
from core.services.user_services import UserService


logger = logging.getLogger(__name__)


class PasswordSignupView(RegisterView):
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password1")
        try:
            user = UserService.create_user(
                email=email, username=username, password=password
            )
        except IntegrityError:
            return Response(
                {
                    "status": "Failed",
                    "message": "user with this Email already exists",
                },
                status.HTTP_409_CONFLICT,
            )
        refresh_token = TokenService.get_refresh_token_for_user(user)
        response = Response(
            {
                "status": "Success",
                "message": "Logged in",
            },
            status.HTTP_200_OK,
        )
        response = TokenService.set_token_in_cookies(refresh_token, response)
        return response


class PasswordLoginView(LoginView):
    def post(self, request) -> Response:
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = PasswordAuthService.login(email, password)
            self.user = user  # let the LoginView know which user it is
        except User.DoesNotExist:
            return Response(
                {
                    "status": "Failed",
                    "message": "User with this email doesn't exist",
                },
                status.HTTP_401_UNAUTHORIZED,
            )
        except AuthenticationFailed:
            return Response(
                {
                    "status": "Failed",
                    "message": "Invalid password",
                },
                status.HTTP_401_UNAUTHORIZED,
            )

        refresh_token = TokenService.get_refresh_token_for_user(self.user)
        response = Response(
            {
                "status": "Success",
                "message": "Logged in",
            },
            status.HTTP_200_OK,
        )

        response = TokenService.set_token_in_cookies(refresh_token, response)
        return response


class TokenRefreshView(APIView):
    def get(self, request) -> Response:
        cookie_refresh_token = request.COOKIES.get("refresh_token")
        try:
            new_refresh = TokenService.renew_refresh_token(cookie_refresh_token)
        except ValueError:
            return Response(
                {
                    "status": "Failed",
                    "message": "Refresh token not present",
                },
                status.HTTP_401_UNAUTHORIZED,
            )
        except TokenError:
            return Response(
                {
                    "status": "Failed",
                    "message": "Invalid refresh token",
                },
                status.HTTP_401_UNAUTHORIZED,
            )
        except User.DoesNotExist:
            return Response(
                {
                    "status": "Failed",
                    "message": "User with this email doesn't exist",
                },
                status.HTTP_401_UNAUTHORIZED,
            )

        response = TokenService.set_token_in_cookies(new_refresh, Response())
        return response


class LogoutView(APIView):
    def get(self, request) -> Response:
        response = Response(
            {
                "status": "Success",
                "message": "Logged Out",
            },
            status.HTTP_200_OK,
        )
        response = TokenService.set_token_in_cookies(None, response)
        return response
