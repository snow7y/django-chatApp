from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm, ChatSessionForm, ChatMessageForm
from .models import ChatSession, ChatMessage

User = get_user_model()



# サインアップ
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


# ホーム
@login_required
def home(request):
    return render(request, 'chat/home.html')


# セッション作成
@login_required
def create_session(request):
    if request.method == 'POST':
        form = ChatSessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('session_detail', session_id=form.instance.id)
    else:
        form = ChatSessionForm()
    return render(request, 'chat/create_session.html', {'form': form})



# セッション詳細
@login_required
def session_detail(request, session_id):
    session = ChatSession.objects.get(id=session_id)
    messages = ChatMessage.objects.filter(session=session).order_by('created_at')

    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.session = session
            message.user = request.user
            message.role = 'user'
            message.save()
            return redirect('session_detail', session_id=session_id)
    else:
        form = ChatMessageForm()

    return render(request, 'chat/session_detail.html', {
        'session': session,
        'messages': messages,
        'form': form
    })