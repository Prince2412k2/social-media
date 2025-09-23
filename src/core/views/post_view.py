import logging
from django.core.exceptions import PermissionDenied
from django.forms import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView

from core.models import Post
from core.serializers.post_serializer import (
    PostIdSerializer,
    GetPostSerializer,
    PostSerializer,
)
from core.services.post_service import PostService


logger = logging.getLogger(__name__)


class PostView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    serializer_class = PostSerializer

    def post(self, request):
        user = request.user
        caption = request.data.get("caption", "")
        image = request.FILES.get("image")
        if not image:
            return Response({"error": "No image provided"}, status=400)
        try:
            post = PostService.create_or_update(
                user=user,
                image_name=image.name,
                image_content=image.read(),
                caption=caption,
            )
        except Exception:
            return Response(
                {"msg": "Something went wrong"}, status=HTTP_400_BAD_REQUEST
            )
        try:
            serialised_post = PostSerializer(post, context={"request": request})
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


class DeletePostView(APIView):
    permission_classes = [IsAuthenticated]

    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    serializer_class = PostIdSerializer

    def post(self, request):
        pk = request.data.get("post_id")
        user = request.user

        try:
            PostService.delete(user, post_id=pk)
        except Post.DoesNotExist:
            return Response(
                {"Status": "Failed", "msg": "Post with given id doesnt exist"},
                status=HTTP_400_BAD_REQUEST,
            )
        except PermissionDenied as e:
            return Response(
                {"Status": "Failed", "msg": str(e)},
                status=HTTP_403_FORBIDDEN,
            )
        return Response(
            {"Status": "Success", "msg": "Deletion successfull"}, status=HTTP_200_OK
        )


class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    serializer_class = PostIdSerializer

    def post(self, request):
        pk = request.data.get("post_id")
        user = request.user

        try:
            PostService.like(user, post_id=pk)
        except Post.DoesNotExist:
            return Response(
                {"Status": "Failed", "msg": "Post with given id doesnt exist"},
                status=HTTP_400_BAD_REQUEST,
            )
        except PermissionDenied as e:
            return Response(
                {"Status": "Failed", "msg": str(e)},
                status=HTTP_403_FORBIDDEN,
            )
        return Response(
            {"Status": "Success", "msg": "Post liked succesfully"}, status=HTTP_200_OK
        )


class UnLikePostView(APIView):
    permission_classes = [IsAuthenticated]

    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    serializer_class = PostIdSerializer

    def post(self, request):
        pk = request.data.get("post_id")
        user = request.user

        try:
            PostService.undislike(user, post_id=pk)
        except Post.DoesNotExist:
            return Response(
                {"Status": "Failed", "msg": "Post with given id doesnt exist"},
                status=HTTP_400_BAD_REQUEST,
            )
        except ValueError:
            return Response(
                {
                    "Status": "Failed",
                    "msg": "you cant dislike a post you havent liked yet",
                },
                status=HTTP_400_BAD_REQUEST,
            )

        except PermissionDenied as e:
            return Response(
                {"Status": "Failed", "msg": str(e)},
                status=HTTP_403_FORBIDDEN,
            )
        return Response(
            {"Status": "Success", "msg": "Post Disliked successfull"},
            status=HTTP_200_OK,
        )
