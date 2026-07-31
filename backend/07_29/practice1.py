"""
practice1.py

說明:
- 使用 Gradio 建立一個簡單的問候介面 (輸入姓名，顯示問候語)
- 需求: 安裝 `gradio` 套件 (pip install gradio)
- 執行: 在此目錄下執行 `python practice1.py`，或使用開發環境直接執行此檔案

檔案重點說明:
- `greet` 函式: 接收 `name` 字串並回傳問候語
- 建立 Gradio 的 `Blocks` UI: 包含一個姓名輸入框、一個輸出框，以及一個按鈕
- 按鈕綁定到 `greet` 函式，點擊後會把輸入的姓名傳入並顯示到輸出框
"""

import gradio as gr


def greet(name: str) -> str:
    """
    產生問候文字並回傳。

    參數:
    - name (str): 使用者輸入的姓名。

    回傳:
    - str: 例如 "Hello Alice!"，若未輸入姓名則回傳通用問候 "Hello!"
    """
    # 處理可能的 None 或空字串，避免發生 TypeError
    if name is None:
        name = ""
    name = str(name).strip()
    if name == "":
        # 若未輸入姓名，回傳通用問候
        return "Hello!"
    # 回傳包含使用者姓名的問候字串
    return "Hello " + name + "!"


# 使用 Gradio Blocks API 建立介面
with gr.Blocks() as demo:
    # `name` 輸入框: 讓使用者輸入姓名
    name = gr.Textbox(label="您的姓名", placeholder="請輸入姓名")
    # `output` 顯示框: 顯示函式回傳的問候語
    output = gr.Textbox(label="輸出結果")
    # 按鈕: 使用者點擊後觸發問候
    greet_btn = gr.Button("送出問候")

    # 綁定按鈕的 click 事件:
    # - fn: 要呼叫的函式 (greet)
    # - inputs: 傳入 greet 的參數 (name Textbox 的值)
    # - outputs: greet 的回傳會顯示在 output Textbox
    # - api_name: (可選) 為此 action 指定 API 名稱，方便用於 Gradio 的 HTTP API
    greet_btn.click(fn=greet, inputs=name, outputs=output, api_name="greet")


# 啟動 Gradio 伺服器，預設會在瀏覽器中開啟界面
# 若要在特定 host/port 或關閉自動開啟瀏覽器，可傳入參數，例如:
# demo.launch(server_name="0.0.0.0", server_port=7860, prevent_thread_lock=False)
demo.launch()