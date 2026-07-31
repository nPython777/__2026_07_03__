"""
practice8.py

說明:
此檔示範如何使用 Gradio Blocks 建立簡單的聊天介面，包含使用者訊息提交、機器人回覆以及對話清空功能。

主要功能:
- 使用 `gr.Chatbot` 顯示對話紀錄。
- 使用 `gr.Textbox` 讓使用者輸入訊息並按 Enter 發送。
- 使用 `gr.State` 保存對話歷史，以便在連續呼叫中傳遞資料。
- 使用 `.submit(...).then(...)` 讓使用者提交訊息後先處理使用者訊息，再接續處理機器人回覆。

使用說明:
1. 安裝 Gradio: `pip install gradio`
2. 執行: `python practice8.py`
3. 在瀏覽器開啟提供的本機網址，輸入訊息後按 Enter 進行對話。
"""

import gradio as gr
import random
import time


def user_action(user_message, history):
    """處理使用者提交的訊息，並更新對話歷史。"""
    history = history or []
    history.append({"role": "user", "content": user_message})
    # 返回空的輸入框值、更新後的 chatbox 歷史和新的 state
    return "", history, history


def bot_action(history):
    """根據對話歷史產生機器人回覆，並將其加入對話歷史中。"""
    history = history or []
    bot_message = random.choice([
        "你好！有什麼我可以幫忙的？",
        "這是一個 Blocks 範例。",
        "很高興為您服務。"
    ])
    # 模擬處理延遲
    time.sleep(1.5)

    history.append({"role": "assistant", "content": bot_message})
    return history, history


with gr.Blocks() as demo:
    # 聊天視窗元件，顯示歷史訊息
    chatbox = gr.Chatbot(label="對話視窗")

    # 輸入欄位：使用者可直接按 Enter 送出訊息
    msg = gr.Textbox(label="請輸入您的訊息（按 Enter 發送）")

    # 清空按鈕：重置聊天歷史與畫面
    clear = gr.Button("🧹 清空對話記錄")

    # 使用 State 存放對話歷史，避免每次提交時遺失先前記錄
    state = gr.State([])

    # 當使用者按 Enter 提交訊息時，先呼叫 user_action 更新對話，
    # 再接續呼叫 bot_action 產生機器人回覆。
    msg.submit(
        fn=user_action,
        inputs=[msg, state],
        outputs=[msg, chatbox, state],
        queue=False,
    ).then(
        fn=bot_action,
        inputs=state,
        outputs=[chatbox, state],
        queue=False,
    )

    # 點擊清空按鈕，將對話視窗和 state 都重置為空列表
    clear.click(
        fn=lambda: ([], []),
        inputs=None,
        outputs=[chatbox, state],
        queue=False,
    )

# 啟動 Gradio 應用
demo.launch()