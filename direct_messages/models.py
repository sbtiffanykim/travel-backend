from django.db import models
from common.models import CommonModel


class ChatRoom(CommonModel):
    """ChatRoom Model Definition"""

    users = models.ManyToManyField("users.User", related_name="chatrooms")

    def __str__(self):
        return "chat room"


class Message(CommonModel):
    """Message Model Definition"""

    text = models.TextField()
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    chat_room = models.ForeignKey("direct_messages.ChatRoom", on_delete=models.CASCADE, verbose_name="chat room")

    def __str__(self):
        return f"{self.user} says: {self.text}"
