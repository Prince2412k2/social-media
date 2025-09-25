from asgiref.sync import sync_to_async
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import User


@sync_to_async
def get_user_from_jwt(token_str) -> User:
    jwt_auth = JWTAuthentication()
    validated_token = jwt_auth.get_validated_token(token_str)
    user = jwt_auth.get_user(validated_token)
    return user


@sync_to_async
def get_token_from_scope(scope):
    return scope["cookies"]["access_token"]


@sync_to_async
def get_room_name(user_id, other_user_id):
    if user_id < other_user_id:
        room_name = f"{user_id}-{other_user_id}"
    else:
        room_name = f"{other_user_id}-{user_id}"

    return f"chat_{room_name}"
