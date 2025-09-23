import logging
from django.core.exceptions import PermissionDenied
from django.forms import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView

from core.serializers.comment_serializer import (
    CommentIdSerializer,
    CommentSerializer,
)
from core.serializers.post_serializer import (
    GetPostSerializer,
    PostIdSerializer,
)
from core.services.comment_service import CommentService


logger = logging.getLogger(__name__)


class CommentView(APIView):
    permission_classes = [IsAuthenticated]

    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    serializer_class = CommentSerializer

    def post(self, request):
        user = request.user
        text = request.data.get("text", "")
        post = request.data.get("post")
        logger.info(request)

        try:
            comment = CommentService.create_or_update(
                user=user, post_id=post, text=text
            )
        except Exception as e:
            logger.info(e)
            return Response(
                {"msg": "Something went wrong"}, status=HTTP_400_BAD_REQUEST
            )
        logger.info(comment)
        try:
            serialised_comment = CommentSerializer(
                comment, context={"request": request}
            )
        except ValidationError:
            return Response(
                {"Status": "Failed", "msg": "Serialization Error"},
                status=HTTP_400_BAD_REQUEST,
            )

        return Response(serialised_comment.data, status=HTTP_200_OK)

    def get(self, request):
        user = request.user
        serialized_user = GetPostSerializer(user, context={"request": request})
        return Response(serialized_user.data, status=HTTP_200_OK)


class GetCommenatsView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    serializer_class = PostIdSerializer

    def post(self, request):
        post_id = request.data.get("post_id")

        try:
            comment = CommentService.get_all(post_id)
        except Exception as e:
            logger.info(e)
            return Response({"msg": str(e)}, status=HTTP_400_BAD_REQUEST)
        try:
            serialised_comments = CommentSerializer(
                comment, context={"request": request}, many=True
            )
        except ValidationError:
            return Response(
                {"Status": "Failed", "msg": "Serialization Error"},
                status=HTTP_400_BAD_REQUEST,
            )

        return Response(serialised_comments.data, status=HTTP_200_OK)

    def get(self, request):
        user = request.user
        serialized_user = GetPostSerializer(user, context={"request": request})
        return Response(serialized_user.data, status=HTTP_200_OK)


class DeleteCommentView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    serializer_class = CommentIdSerializer

    def post(self, request):
        user = request.user
        comment_id = request.data.get("comment_id")

        try:
            CommentService.delete(user=user, comment_id=comment_id)
        except PermissionDenied:
            return Response(
                {
                    "Status": "failed",
                    "msg": "You do no have permission to delete this comment",
                },
                status=HTTP_401_UNAUTHORIZED,
            )

        except ValueError as e:
            return Response(
                {"Status": "failed", "msg": str(e)}, status=HTTP_400_BAD_REQUEST
            )
        return Response(
            {"Status": "Success", "msg": "Comment Deleted"}, status=HTTP_200_OK
        )

    def get(self, request):
        user = request.user
        serialized_user = GetPostSerializer(user, context={"request": request})
        return Response(serialized_user.data, status=HTTP_200_OK)
