import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.views import LoginView
from core.auth.password_service import verify_password
from core.models import User
from social.settings import SIMPLE_JWT


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
