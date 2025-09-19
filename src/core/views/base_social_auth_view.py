import logging
from typing import Type
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError
from dj_rest_auth.registration.views import SocialLoginView
from django.db import IntegrityError

from core.models import Credential, Provider_Type
from core.services.base_auth_service import BaseAuthService
from core.services.token_service import TokenService

logger = logging.getLogger(__name__)


class BaseSocialAuthView(SocialLoginView):
    auth_service: Type[BaseAuthService]
    provider: Provider_Type

    def get(self, request):
        code = request.query_params.get("code", False)
        if not code:
            return Response(
                {"error": "No 'code' field fount in query"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        token = self.auth_service.get_token_from_code(code)
        return self.common_response(token)

    def post(self, request):
        token = request.data.get("id_token")
        if not token:
            return Response(
                {
                    "status": "Failed",
                    "message": f"{self.provider} auth token retrieval error",
                },
                status.HTTP_400_BAD_REQUEST,
            )
        return self.common_response(token)

    def common_response(self, id_token):
        try:
            user = self.auth_service.get_user_from_token(id_token=id_token)
        except TokenError:
            return Response(
                {
                    "status": "Failed",
                    "message": f"Invalid {self.provider} auth Token",
                },
                status.HTTP_400_BAD_REQUEST,
            )
        except IntegrityError:
            return Response(
                {
                    "status": "Failed",
                    "message": "User with given email already exists",
                },
                status.HTTP_409_CONFLICT,
            )

        response = Response(
            {
                "status": "Success",
                "message": "Logged in",
            },
            status.HTTP_200_OK,
        )
        refresh_token = TokenService.get_refresh_token_for_user(user)
        response = TokenService.set_token_in_cookies(refresh_token, response)
        response = TokenService.set_token_in_cookies(refresh_token, response)
        return response
