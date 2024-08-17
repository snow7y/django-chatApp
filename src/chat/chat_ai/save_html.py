from typing import Type
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool
import uuid
import logging
import os

logger = logging.getLogger(__name__)


def save_html_to_file(html_content, save_dir_name="generated_files"):
    # ユニークなIDを生成する
    unique_id = str(uuid.uuid4())
    # ファイル名を作成する
    file_name = f"{unique_id}.html"
    # ディレクトリが存在しない場合は作成する
    save_dir = os.path.join("chat/templates/chat", save_dir_name)
    os.makedirs(save_dir, exist_ok=True)
    # フルパスを作成する
    file_path = os.path.join(save_dir, file_name)
    # HTMLコンテンツをファイルに書き込む
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(html_content)
    
    # 書き込んだファイルの絶対パスを取得する
    file_link = f"localhost:8000/view_html/{file_name}"

    # ファイルへのリンクを返す
    return file_link


class SaveHtmlToFileInput(BaseModel):
    html_content: str = Field(
        description="保存したいHTMLコンテンツ。htmlのコードのみを受け付ける example: <html><body><h1>Hello World</h1></body></html>",)


class SaveHtmlToFileTool(BaseTool):
    name = "save_html_to_file_tool"
    description = "HTMLコンテンツをファイルに保存するツール 保存したいHTMLコンテンツを受け取り、ファイルに保存をし保存したファイルを表示するためのURLを返します"
    args_schema: Type[BaseModel] = SaveHtmlToFileInput

    def _run(
            self,
            html_content: str,
    ) -> str:
        """use the tool."""
        try:
            print(f"save_html_to_file_toolが次の値で呼び出されました: {html_content}")
            result_url = save_html_to_file(html_content)
            return result_url
        except Exception as e:
            res = f"エラーが発生しました: {e}"
            print(res)
            return res


save_html_to_file_tool = SaveHtmlToFileTool()

# 使用例
if __name__ == "__main__":
    html_code = "<html><body><h1>Hello World</h1></body></html>"
    file_link = save_html_to_file_tool.invoke({"html_content": html_code})
    print(f"HTML file saved at: {file_link}")
