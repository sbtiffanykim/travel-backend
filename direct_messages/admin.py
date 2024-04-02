from django.contrib import admin
from .models import Message, ChatRoom


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("text", "user", "chat_room", "created_date")


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("__str__", "updated_date")
