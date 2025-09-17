from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models import User
from ..serializer import UserSerializer


@api_view(["GET"])
def get_users(request):
    """
    GET : serialized user|users objects
    given pk it return user with pk
    without pk it returns all users
    """
    user = User.objects.all()
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user(request):
    users = request.user
    serializer = UserSerializer(users)
    return Response(serializer.data)


# NOTE :get is here only for html forms in DRF dashboard
@api_view(["GET", "POST"])
def create_user(request):
    """
    POST : create a new user
    """
    if request.method == "POST":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializer()
    return Response(serializer.data)


@api_view(["PUT"])
def put_user(request, pk):
    """
    PUT : edit user with pk
    """
    try:
        user = get_user_by_id(pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_user(pk):
    """
    DELETE : delete user with pk
    """
    try:
        user = get_user_by_id(pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def get_user_by_id(pk):
    """
    get user by its primary key:pk
    """
    return User.objects.get(pk=pk)


# Create your views here.
