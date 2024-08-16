from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


from .forms import CustomUserCreationForm, ChatSessionForm, ChatMessageForm
from .models import ChatSession, ChatMessage
import os

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
    sessions = ChatSession.objects.filter(messages__user=request.user).distinct().order_by('-created_at')

    if request.method == 'POST':
        form = ChatSessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('session_detail', session_id=form.instance.id)
    else:
        form = ChatSessionForm()

    return render(request, 'chat/home.html', {'sessions': sessions, 'form': form})


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

            # AIからの返答を追加
            ai_message_content = get_ai_response(message.content)  # AIメッセージの生成
            ai_message = ChatMessage(
                session=session,
                user=request.user,  # 将来的にはAIユーザーに変更
                content=ai_message_content,
                role='ai'
            )
            ai_message.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'username': message.user.username,
                    'content': message.content,
                    'role': message.role,
                    'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'ai_response': {
                        'username': 'AI',
                        'content': ai_message.content,
                        'role': ai_message.role,
                        'created_at': ai_message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    }
                })
            return redirect('session_detail', session_id=session_id)
    else:
        form = ChatMessageForm()

    return render(request, 'chat/session_detail.html', {
        'session': session,
        'messages': messages,
        'form': form
    })


def get_ai_response(user_message):
    # AI応答を生成するロジック
    # 将来的にはChatGPT APIを使用する予定
    return "AIの固定応答: " + user_message


def view_html(request, file_id):
    # ファイルIDからファイルのURLを取得
    file_url = f"http://localhost:8000/view_html/iframe/{file_id}"
    return render(request, 'chat/view_html.html', {'file_url': file_url})

def view_html_iframe(request, file_id):
    # ファイルIDのHTMLファイルがあるか確認
    if not os.path.exists(f"src/chat/templates/chat/generated_files/{file_id}.html"):
        return render(request, '404.html', {'error': 'ファイルが見つかりませんでした'})
    return render(request, f"chat/generated_files/{file_id}.html")