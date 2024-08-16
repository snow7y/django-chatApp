from typing import Type
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool
import uuid
import logging
import os

logger = logging.getLogger(__name__)


def save_html_to_file(html_content, save_dir="html_files"):
    # ユニークなIDを生成する
    unique_id = str(uuid.uuid4())
    # ファイル名を作成する
    file_name = f"{unique_id}.html"
    # ディレクトリが存在しない場合は作成する
    os.makedirs(save_dir, exist_ok=True)
    # フルパスを作成する
    file_path = os.path.join(save_dir, file_name)
    # 現在の相対パスを絶対パスに置き換える
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # HTMLコンテンツをファイルに書き込む
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(html_content)

    # ファイルへのリンクを返す
    return f"{current_dir}/{file_path}"


class SaveHtmlToFileInput(BaseModel):
    html_content: str = Field(
        description="保存したいHTMLコンテンツ example: <html><body><h1>Hello World</h1></body></html>")


class SaveHtmlToFileTool(BaseTool):
    name = "save_html_to_file_tool"
    description = "HTMLコンテンツをファイルに保存するツール 保存したいHTMLコンテンツを受け取り、ファイルに保存をし保存したファイルを表示するためのURLを返します"
    args_schema: Type[BaseModel] = SaveHtmlToFileInput

    def _run(
            self,
            html_content: str,
    ) -> str:
        """use the tool."""
        logger.info(f"save_html_to_file_toolが次の値で呼び出されました: {html_content}")
        result_url = save_html_to_file(html_content)
        return result_url


save_html_to_file_tool = SaveHtmlToFileTool()

# 使用例
if __name__ == "__main__":
    with open("index.html", "r", encoding="utf-8") as file:
        html_code = file.read()
    # html_code = "<html><body><h1>Hello World</h1></body></html>"
    file_link = save_html_to_file_tool.invoke({"html_content": html_code})
    print(f"HTML file saved at: {file_link}")
