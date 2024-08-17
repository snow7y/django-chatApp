from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import AzureChatOpenAI
from langchain.agents import AgentExecutor
from langchain.agents import create_tool_calling_agent
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.tools import DuckDuckGoSearchRun
from .save_html import SaveHtmlToFileTool
import os
from dotenv import load_dotenv
load_dotenv(override=True)


system_template = """あなたは熟練のフロントエンジニアです。
ユーザーからの要望に応じて要件をまとめ、HTMLファイルを作成することができます。

あなたがやるべきこと:
- ユーザーからの要望を受け取る
- 要件をまとめる
- 要件に応じたHTMLファイルを作成する
- Toolを使用し作成したHTMLファイルのURLをユーザーに返す

作成するHTMLファイルのルール:
- 作成するHTMLファイルは必ず次のheadタグを持つ
```html
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bootstrap demo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
</head>
```
- デザインはBootstrapを使用し、必要な場合のみjsを追加する
- 作成したHTMLコードのみToolに渡しそれ以外は渡さないようにする

作成するHTMLファイルの例:
<!doctype html>
<html lang="ja">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Bootstrap demo</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
    </head>
    <body>
        <h1>Hello World</h1>
        <p class="text>こんにちは、世界</p>
    </body>
</html>


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
# エージェントの使用できるツール
search = DuckDuckGoSearchRun()
save_html_to_file_tool = SaveHtmlToFileTool()
tools = [save_html_to_file_tool, search]


# エージェントのもとを作成
agent = create_tool_calling_agent(llm, tools, prompt)

# エージェントがToolを実行できるようにする
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


def add_chat_history(role, input_message: str, chat_history=[]):
    if role == "user":
        chat_history.append(HumanMessage(input_message))
    else:
        chat_history.append(AIMessage(input_message))
    return chat_history


def run_agent(input_message: str, chat_history=[]) -> dict:
    try:
        print(f"次の値でエージェントを実行します: {input_message}, chat_history: {chat_history}")
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
