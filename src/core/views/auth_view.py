import logging
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import User

logger = logging.getLogger(__name__)


##JWT_TOKEN_VIEW
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            email=email,
            password=password,
        )
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        data = super().validate(attrs)
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


## REFRESH TOKEN VIEW
class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = RefreshToken(attrs["refresh"])

        user_id = refresh["user_id"]
        try:
            user = User.all_objects.get(pk=user_id)  # use unfiltered manager
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found for this token.")

        self.user = user
        # Build response (new access + optionally refresh)
        data = {"access": str(refresh.access_token)}

        if self.token_class.lifetime:
            data["refresh"] = str(refresh)
        return data


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer
