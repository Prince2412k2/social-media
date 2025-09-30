from django.urls import path
from .views import ws_view, GetInbox, GetChat

urlpatterns = [
    # When a user navigates to the URL assigned to this app (e.g., /home/),
    # Django executes the 'home_view' function.
    path("", ws_view, name="ws"),
    path("inbox/", GetInbox.as_view(), name="get-inbox"),
    path("messages", GetChat.as_view(), name="get-chat"),
]
