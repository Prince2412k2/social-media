from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.serializers.user_serializer import DBUserSerializer

from ..models import User


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
