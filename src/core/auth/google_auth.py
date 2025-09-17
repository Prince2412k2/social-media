import logging
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from core.models import Credential, User
import requests
from django.db import transaction

from social.settings import GOOGLE_CLIENT_ID


logger = logging.getLogger(__name__)


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
