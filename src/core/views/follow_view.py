from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from core.serializers.user_serializer import DBUserSerializer
from core.serializers.follow_serializer import FollowSerializer
from core.services.user_services import FollowService
from ..models import User


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def FollowUserView(request):
    self_user = request.user
    serializer = FollowSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    try:
        FollowService.follow(self_user, serializer.validated_data["user_id"])
    except User.DoesNotExist:
        return Response(
            {
                "status": "Failed",
                "message": "User with given id doesn't exist",
            },
            status.HTTP_404_NOT_FOUND,
        )
    return Response({"Status": "Success"}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def UnfollowUserView(request):
    self_user = request.user
    serializer = FollowSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    try:
        FollowService.unfollow(self_user, serializer.validated_data["user_id"])
    except User.DoesNotExist:
        return Response(
            {
                "status": "Failed",
                "message": "User with given id doesn't exist",
            },
            status.HTTP_404_NOT_FOUND,
        )
    except ValueError as msg:
        return Response(
            {
                "status": "Failed",
                "message": msg,
            },
            status.HTTP_404_NOT_FOUND,
        )
    return Response({"Status": "Success"}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def RemoveFollower(request):
    self_user = request.user
    serializer = FollowSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    try:
        FollowService.remove_follower(self_user, serializer.validated_data["user_id"])
    except User.DoesNotExist:
        return Response(
            {
                "status": "Failed",
                "message": "User with given id doesn't exist",
            },
            status.HTTP_404_NOT_FOUND,
        )
    except ValueError as msg:
        return Response(
            {
                "status": "Failed",
                "message": msg,
            },
            status.HTTP_404_NOT_FOUND,
        )
    return Response({"Status": "Success"}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def GetFollowers(request):
    self_user = request.user
    users = FollowService.get_followers(self_user)
    serializered_users = DBUserSerializer(users, many=True)
    return Response(
        {"Status": "Success", "followers": serializered_users.data},
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def GetFollowing(request):
    self_user = request.user
    users = FollowService.get_following(self_user)
    serializered_users = DBUserSerializer(users, many=True)
    return Response(
        {"Status": "Success", "followers": serializered_users.data},
        status=status.HTTP_200_OK,
    )
