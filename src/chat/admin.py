from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import ChatSession, ChatMessage

User = get_user_model()

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass

admin.site.register(ChatSession)
admin.site.register(ChatMessage)
