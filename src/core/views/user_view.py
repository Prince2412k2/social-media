import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView

from core.serializers.user_serializer import (
    DBUserSerializer,
    RequestUpdateUserSerializer,
)
from core.services.user_services import UserService

from ..models import User

logger = logging.getLogger(__name__)


@api_view(["GET"])
def get_users(request) -> Response:
    user = User.objects.all()
    serializer = DBUserSerializer(user, many=True)
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
        except Exception as e:
            return Response({"msg": "error"}, status=HTTP_400_BAD_REQUEST)
        return Response({"msg": "success"}, status=HTTP_200_OK)

    def get(self, request):
        user = request.user
        # TODO:Handle proper excepttions
        try:
            serializer = RequestUpdateUserSerializer(user)
            data = serializer.data
        except Exception as e:
            return Response({"msg": "error"}, status=HTTP_400_BAD_REQUEST)

        return Response(data, status=HTTP_200_OK)
