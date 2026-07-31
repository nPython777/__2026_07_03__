"""
practice2.py

說明:
此檔案示範另一種使用 Gradio Blocks API 的寫法：
- 提供姓名輸入框與輸出欄位，按下按鈕後將顯示問候語。

快速使用:
1. 安裝 Gradio：`pip install gradio`
2. 執行：`python practice2.py`
3. 在終端看到的本機網址（例如 http://127.0.0.1:7860）中開啟介面，輸入姓名後按下按鈕查看結果。

程式說明:
- `gr.Textbox` 作為輸入與輸出元件。
- `gr.Button` 綁定按鈕事件，使用 `@button.click(inputs=..., outputs=...)` 裝飾函式，將輸入傳入函式並把回傳值顯示到輸出元件。

注意:
- 函式內做了簡單的輸入檢查以避免空值導致不友善顯示。
"""

import gradio as gr

with gr.Blocks() as demo:
    # 使用者輸入姓名的文字欄位
    name = gr.Textbox(label="您的姓名")

    # 顯示問候結果的文字欄位
    output = gr.Textbox(label="輸出結果")

    # 送出按鈕，按下後會呼叫 greet 函式
    greet_btn = gr.Button("送出問候")

    @greet_btn.click(inputs=name, outputs=output)
    def greet(name: str) -> str:
        """接收使用者輸入的姓名並回傳問候訊息。

        參數:
            name (str): 使用者輸入的文字，可能為空或 None。

        回傳:
            str: 若有有效姓名回傳問候；否則回傳提醒用戶輸入姓名。
        """
        if name is None:
            return "請輸入您的姓名後再按送出。"

        name_str = str(name).strip()
        if name_str == "":
            return "請輸入您的姓名後再按送出。"

        # 保留原先的英文問候，並確保輸入已去除前後空白
        return "Hello " + name_str + "!"

# 啟動 Gradio 介面（預設在本機啟動伺服器）
demo.launch()