import logging
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.views import APIView

from chatapp.serializers.chat_serializer import InboxSerializer, MessageSerializer
from chatapp.services.chat_service import ChatService
from core.services.user_services import UserService

logger = logging.getLogger(__name__)


def ws_view(request):
    return render(request, "chatapp/index.html", {})


class GetInbox(APIView):
    permission_classes = [IsAuthenticated]

    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request):
        people = ChatService.get_chat_partners(request.user)
        serialized = InboxSerializer(people, many=True)
        print(serialized.data)
        return Response(serialized.data)


class GetChat(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def post(self, request):
        other_user_id = request.data.get("user_id")
        if not other_user_id:
            return Response({"status": "Failed", "msg": "user_id is required Field"})
        other_user = UserService.get_user_by_pk(other_user_id)
        chats = ChatService.get_messages_between(request.user, other_user)
        serialized_chats = MessageSerializer(chats, many=True)
        return Response(serialized_chats.data)
