from django.contrib import admin
from .models import User, ChatSession, ChatMessage

admin.site.register(User)
admin.site.register(ChatSession)
admin.site.register(ChatMessage)
