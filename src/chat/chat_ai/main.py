from save_html import save_html_to_file_tool
import os
from dotenv import load_dotenv
load_dotenv()

main_agent_tools = [save_html_to_file_tool]
main_agent_info = """あなたは熟練のフロントエンジニアです。
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


class MainAgent(Agent):
    def __init__(
            self,
            llm: AzureChatOpenAI = llm,
            user_info: User = User(),
            assistant_info: str = main_agent_info,
            tools: list = main_agent_tools,
    ):
        super().__init__(
            llm=llm,
            user_info=user_info,
            assistant_info=assistant_info,
            tools=tools
        )


if __name__ == "__main__":
    main_agent = MainAgent()
    print(main_agent.get_agent_info())
    print(main_agent.invoke("簡単なブログサイトを作成してください。"))
