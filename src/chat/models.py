from django.db import models
from django.contrib.auth.models import AbstractUser


# ユーザーモデル
class User(AbstractUser):
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='chat_users',  # ここに related_name を追加
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='chat_users',  # ここに related_name を追加
        blank=True
    )


# チャットセッションモデル
class ChatSession(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# チャットモデル
class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    role = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content}'
