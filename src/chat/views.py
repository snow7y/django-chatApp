from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


from .forms import CustomUserCreationForm, ChatSessionForm, ChatMessageForm
from .models import ChatSession, ChatMessage
import os

from .chat_ai.main import add_chat_history, run_agent

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

@login_required
def delete_session(request, session_id):
    session = ChatSession.objects.get(id=session_id)
    session.delete()
    return redirect('home')



# セッション詳細
@login_required
def session_detail(request, session_id):
    session = ChatSession.objects.get(id=session_id)
    messages = ChatMessage.objects.filter(session=session).order_by('created_at')

    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            # もし過去にチャット履歴がある場合は追加する
            chat_history = []
            if messages:
                for chat_message in messages:
                    chat_history = add_chat_history(chat_message.role, chat_message.content, chat_history)
            # AIからの返答を追加
            message = form.save(commit=False)
            message.session = session
            message.user = request.user
            message.role = 'user'
            message.save()

            # エージェントを実行
            # ai_response = run_agent(message.content, chat_history)
            
            ai_response = run_agent(message.content, chat_history, dummy=True) # dummy=Trueでエラーを発生させLLMの料金を節約
            # ai_response = run_agent(message.content, chat_history)
            ai_message = ChatMessage(
                session=session,
                user=request.user,  # 将来的にはAIユーザーに変更
                content=ai_response['output'],
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



def view_html(request, file_id):
    # もしファイルIDが.htmlで終わっている場合は取り除く
    if file_id.endswith(".html"):
        file_id = file_id[:-5]

    # ファイルIDからファイルのURLを取得
    file_url = f"http://127.0.0.1:8000//view_html/iframe/{file_id}"
    return render(request, 'chat/view_html.html', {'file_url': file_url})

def view_html_iframe(request, file_id):
    # ファイルIDのHTMLファイルがあるか確認
    file_path = f"chat/templates/chat/generated_files/{file_id}.html"
    if not os.path.exists(file_path):
        print(f"次のファイルが見つかりませんでした: {file_path}")
        return render(request, '404.html', {'error': 'ファイルが見つかりませんでした'})
    return render(request, f"chat/generated_files/{file_id}.html")