from django.urls import re_path
from chatapp.consumers import MyConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<other_user_id>\w+)/$", MyConsumer.as_asgi()),
]
