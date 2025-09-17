from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Credential, User
from ..serializer import CredentialSerializer


@api_view(["GET"])
def credentials(request):
    """
    get all users as a list of objects
    """
    return get_credentials(pk=None)


# Create your views here.
def get_credentials(pk=None):
    """
    GET : serialized user/users objects
    given pk it return user with pk
    without pk it returns all users
    """
    if not pk:
        users = Credential.objects.all()
        serializer = CredentialSerializer(users, many=True)
        return Response(serializer.data)
    else:
        cred = Credential.objects.get(pk=pk)
        serializer = CredentialSerializer(cred)
        return (
            Response(serializer.data)
            if not cred.is_deleted
            else Response(status=status.HTTP_404_NOT_FOUND)
        )
