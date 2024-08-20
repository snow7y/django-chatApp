from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import AzureChatOpenAI
from langchain.agents import AgentExecutor
from langchain.agents import create_tool_calling_agent
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.tools import DuckDuckGoSearchRun
from .save_html import SaveHtmlToFileTool
import os
from dotenv import load_dotenv

try:
    load_dotenv(override=True)
    # Azure Chat OpenAIのクライアントを作成
    llm = AzureChatOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_deployment=os.environ['AZURE_DEPLOYMENT_NAME'],  # Azureリソースのデプロイメント名
        api_version=os.environ['OPENAI_API_VERSION'],  # azure openaiのAPIバージョン
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
except Exception as e:
    print(f"環境変数を読み込めませんでした: {e}")
    llm = None


system_template = """あなたはプロフェッショナルなフロントエンドエンジニアとして、ユーザーの要望に基づいて高品質なHTMLファイルを作成します。以下の手順とルールに従って作業を進めてください。

# あなたの役割とタスク:
- ユーザーの要望を正確に把握する: 要件を明確にし、必要な機能やデザインの詳細を確認します。
- 要件を整理し、具体的な仕様を策定する: 使用する技術やデザインの方向性を決定します。
- HTMLファイルを作成する: 以下のルールに従い、要件に合致したHTMLコードを生成します。
- 生成したHTMLコードをToolに渡し、URLを取得してユーザーに返す: コードのみをToolに渡し、他の情報は含めないようにします。

# HTMLファイル作成のルール:
- 必須のheadタグ: 以下のheadタグを必ず含めてください。
```html
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bootstrap demo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
    <style>
        /* 必要に応じてモダンなデザインを実現するための追加CSSをここに記述 */
    </style>
</head>
```
- デザインフレームワーク: Bootstrapを使用し、必要に応じて`<style>`タグで追加のCSSを適用します。デザインはモダンで、UXを最大限に引き出すことを目指してください。
- ベストプラクティス:
    - カスタムテーマの作成: BootstrapのSass変数をカスタマイズして、色、タイポグラフィ、スペーシングをプロジェクトのブランドに合わせて調整します。
    - CSS Gridの活用: BootstrapのFlexboxベースのグリッドシステムに加えて、CSS Gridを使用して複雑なレイアウトを実現します。
    - アニメーションとマイクロインタラクション: BootstrapのアニメーションクラスやAnimate.cssなどのライブラリを活用して、ユーザー体験を向上させるアニメーションを追加します。
    - インタラクティブなコンポーネント: モーダル、ツールチップ、カルーセルなどのBootstrapコンポーネントを活用し、インタラクティブなUIを構築します。
    - レスポンシブデザイン: Bootstrapのグリッドシステムを使用して、デバイスに応じたレスポンシブなレイアウトを作成します。

# 作成するHTMLファイルの例:
```html
<!doctype html>
<html lang="ja">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Bootstrap demo</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
        <style>
            /* モダンなデザインを実現するためのCSS */
        </style>
    </head>
    <body>
        <h1>Hello World</h1>
        <p class="text">こんにちは、世界</p>
    </body>
</html>
```
"""

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            system_template,
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)


# エージェントの使用できるツール
search = DuckDuckGoSearchRun()
save_html_to_file_tool = SaveHtmlToFileTool()
tools = [save_html_to_file_tool, search]







def add_chat_history(role, input_message: str, chat_history=[]):
    if role == "user":
        chat_history.append(HumanMessage(input_message))
    else:
        chat_history.append(AIMessage(input_message))
    return chat_history


def run_agent(input_message: str, chat_history=[]) -> dict:
    try:
        if llm is None:
            return {'output': '環境変数が設定されていません。設定しなおしたうえで再起動してください。'}
        print(
            f"次の値でエージェントを実行します: {input_message}, chat_history: {chat_history}")
        
        # エージェントのもとを作成
        agent = create_tool_calling_agent(llm, tools, prompt)
        # エージェントがToolを実行できるようにする
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        return agent_executor.invoke({"input": input_message, "chat_history": chat_history})
    
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return {'output': 'エラーが発生しました'}


if __name__ == "__main__":
    input_message = "要件はブログのタイトルと最終更新日時、概要をカード形式で表示するような感じです。デザインはシンプルで見やすいものがいいです。"
    chat_history = add_chat_history("user", 'ブログサイトを作成して')
    chat_history = add_chat_history(
        "ai", 'ブログサイトを作成するための要件を教えてください。どのような機能やデザインが必要ですか？', chat_history)
    result = run_agent(input_message, chat_history)
    print(result)
    print(result['output'])
