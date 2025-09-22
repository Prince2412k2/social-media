import logging
from django.forms import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from core.models import Comment
from core.serializers.comment_serializer import CommentSerializer
from core.serializers.post_serializer import (
    GetPostSerializer,
    PostSerializer,
)
from core.services.comment_service import CommentService


logger = logging.getLogger(__name__)


class CommentView(APIView):
    permission_classes = [IsAuthenticated]

    serializer_class = CommentSerializer

    def post(self, request):
        user = request.user
        text = request.data.get("text", "")
        post = request.data.get("post")
        logger.info(request)
        logger.info(post)

        try:
            post = CommentService.create_or_update(user=user, post_id=post, text=text)
        except Exception as e:
            logger.info(e)
            return Response(
                {"msg": "Something went wrong"}, status=HTTP_400_BAD_REQUEST
            )
        try:
            serialised_post = CommentSerializer(post, context={"request": request})
        except ValidationError:
            return Response(
                {"Status": "Failed", "msg": "Serialization Error"},
                status=HTTP_400_BAD_REQUEST,
            )

        return Response(serialised_post.data, status=HTTP_200_OK)

    def get(self, request):
        user = request.user
        serialized_user = GetPostSerializer(user, context={"request": request})
        return Response(serialized_user.data, status=HTTP_200_OK)
