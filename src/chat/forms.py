from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ChatSession, ChatMessage

class CustomUserCreationForm(UserCreationForm):
    """Extending default user creation form"""

    class Meta:
        #Use our user model in creationform
        model = User
        fields = ['username']

class ChatSessionForm(forms.ModelForm):
    class Meta:
        model = ChatSession
        fields = ['name']

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['content']