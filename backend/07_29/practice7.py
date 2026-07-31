"""
practice7.py

說明:
此檔案示範 Gradio 中的 `gr.skip()` 用法，讓一個回傳值保持元件原有內容不變。
範例中有兩個數值元件 `數值 A` 與 `數值 B`，共有三個按鈕:
- 清除：將兩個數值欄位全部清空為 None。
- 跳過 A：只修改 `數值 B` 的值為固定 10，並保持 `數值 A` 原本內容不變。
- 隨機產生：同時為兩個欄位產生新的隨機整數。

使用說明:
1. 安裝 Gradio: `pip install gradio`
2. 執行: `python practice7.py`
3. 在瀏覽器中開啟提供的本機網址，按鈕操作並觀察元件值的變化。
"""

import random
import gradio as gr

with gr.Blocks() as demo:
    # 將三個按鈕放在同一列中顯示
    with gr.Row():
        clear_button = gr.Button("清除")
        skip_button = gr.Button("跳過 A (保持原狀)")
        random_button = gr.Button("隨機產生")

    # 建立兩個數值元件，用於顯示和回傳按鈕結果
    numbers = [gr.Number(label="數值 A"), gr.Number(label="數值 B")]

    # 清除按鈕：將 A、B 兩個欄位都清空
    clear_button.click(lambda: (None, None), outputs=numbers)

    # 跳過按鈕：使用 gr.skip() 表示保留 A 的原值，僅更新 B 為 隨機數
    skip_button.click(lambda: [gr.skip(), random.randint(0, 100)], outputs=numbers)

    # 隨機產生按鈕：一次更新 A 和 B 兩個欄位為新的隨機整數
    random_button.click(
        lambda: (random.randint(0, 100), random.randint(0, 100)),
        outputs=numbers
    )

# 啟動 Gradio 介面
demo.launch()