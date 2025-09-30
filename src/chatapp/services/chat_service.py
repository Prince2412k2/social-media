from django.contrib.auth import get_user_model
from django.db.models import Max
from chatapp.models import Conversation, Message

user_model = get_user_model()


class ChatService:
    @staticmethod
    def get_chat_partners(user):
        conversations = Conversation.objects.filter(participants=user)

        partners = (
            user_model.objects.filter(conversations__in=conversations)
            .exclude(id=user.id)
            .distinct()
        )
        partners = partners.annotate(
            last_chat=Max("conversations__created_at")
        ).order_by("-last_chat")
        return partners

    @staticmethod
    def get_messages_between(user1, user2):
        conversation = (
            Conversation.objects.filter(participants=user1)
            .filter(participants=user2)
            .first()
        )
        if not conversation:
            return Message.objects.none()
        messages = conversation.messages.order_by("timestamp")
        return messages
