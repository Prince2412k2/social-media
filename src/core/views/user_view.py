import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView

from core.serializers.user_serializer import (
    DBUserSerializer,
    RequestUpdateUserSerializer,
)
from core.services.user_services import UserService

from ..models import User

logger = logging.getLogger(__name__)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def get_user_by_id(request) -> Response:
    user_id = request.data.get("user_id")
    user = UserService.get_user_by_pk(user_id)
    serializer = DBUserSerializer(user)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user(request) -> Response:
    users = request.user
    serializer = DBUserSerializer(users)
    return Response(serializer.data)


class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    serializer_class = RequestUpdateUserSerializer

    def put(self, request):
        user = request.user
        avatar = request.FILES.get("avatar")
        username = request.data.get("username", None)
        email = request.data.get("email", None)
        bio = request.data.get("bio", None)

        try:
            # TODO:Handle proper excepttions
            UserService.update(
                user=user, avatar=avatar, email=email, username=username, bio=bio
            )
        except User.DoesNotExist:
            return Response(
                {"status": "Failed", "msg": "User with given id doesnt exist"}
            )
        return Response({"status": "success", "msg": "success"}, status=HTTP_200_OK)

    def get(self, request):
        user = request.user
        # TODO:Handle proper excepttions
        try:
            serializer = RequestUpdateUserSerializer(user)
            data = serializer.data
        except User.DoesNotExist:
            return Response(
                {"status": "Failed", "msg": "User with given id doesnt exist"},
                status=HTTP_404_NOT_FOUND,
            )
        except ValidationError:
            return Response(
                {"status": "Failed", "msg": "Invalid request format"},
                status=HTTP_400_BAD_REQUEST,
            )
        return Response(data, status=HTTP_200_OK)
