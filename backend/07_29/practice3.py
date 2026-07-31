import gradio as gr

"""
practice3.py

說明:
此檔案示範如何使用 Gradio 的 Blocks API 建立一個簡單的即時互動介面。
使用者在文字輸入框輸入姓名後，輸出欄位會即時顯示歡迎訊息。

快速上手:
1. 建議建立虛擬環境並安裝相依套件：`pip install gradio`
2. 在該目錄執行：`python practice3.py`
3. 開啟終端輸出提供的本機網址（通常是 http://127.0.0.1:7860）即可在瀏覽器使用。

程式架構說明:
- 使用 `gr.Blocks()` 作為元件容器，便於管理多個元件與事件。
- 使用 `gr.Markdown()` 顯示頁首說明文字。
- 使用 `gr.Textbox()` 建立輸入與輸出元件。
- 使用事件裝飾器 `@inp.change(...)`，當輸入元件內容變更時呼叫對應函式，並將結果顯示到指定輸出元件。

注意:
- 若需公開分享，可在 `demo.launch(share=True)` 中啟用外部分享（會上傳至 Gradio 服務）。
"""

with gr.Blocks() as demo:
    # 頁首說明（可使用 Markdown）
    gr.Markdown("# 👋 歡迎頁面\n請在下方輸入您的姓名，輸出將即時更新：")

    # 文字輸入元件：使用者在此輸入姓名
    inp = gr.Textbox(placeholder="您叫什麼名字？", label="文字輸入")

    # 文字輸出元件：顯示即時歡迎詞
    out = gr.Textbox(label="即時歡迎詞")

    @inp.change(inputs=inp, outputs=out)
    def welcome(name: str) -> str:
        """當輸入框內容變更時被呼叫，回傳要顯示在輸出欄位的字串。

        參數:
            name (str): 使用者在輸入欄位輸入的姓名。

        回傳:
            str: 若有輸入內容則回傳歡迎訊息；否則回傳提醒文字。
        """
        # 處理空字串或僅有空白的情況
        if name is None:
            return "請輸入您的姓名。"

        name_str = str(name).strip()
        if name_str == "":
            return "請輸入您的姓名。"

        # 回傳格式化的歡迎訊息
        return f"歡迎來到 Gradio，{name_str}！"

# 啟動 Gradio 應用（可傳入參數如 `share=True`）
demo.launch()