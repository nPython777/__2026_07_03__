"""
practice6.py

示範如何在 Gradio Blocks 中動態更新已存在元件的屬性（例如顯示/隱藏、行數、標籤等）。

使用說明：
1. 安裝 Gradio：`pip install gradio`
2. 執行：`python practice6.py`
3. 在瀏覽器中打開提供的本機網址，選擇不同寫作模式觀察文字欄位如何變化。

設計重點：
- 使用 `@radio.change(...)` 綁定當 `radio` 選項改變時觸發的處理函式。
- 建議回傳 `component.update(...)` 物件以只修改元件屬性，而不是建立新的元件物件。
"""

import gradio as gr

with gr.Blocks() as demo:
    # 單選元件：選擇寫作模式
    radio = gr.Radio(
        ["短文模式", "長文模式", "隱藏"],
        label="請選擇寫作模式"
    )

    # 單一文字欄位，初始為短文 (2 行)，可互動
    text = gr.Textbox(lines=2, interactive=True, label="寫作欄位")

    @radio.change(inputs=radio, outputs=text)
    def change_textbox(choice: str):
        """根據 radio 的選擇動態更新 `text` 元件的屬性。

        參數:
            choice (str): 使用者在 radio 中選擇的選項。

        回傳:
            gr.update: 使用 `text.update(...)` 回傳要變更的屬性。
        """
        # 處理 None 或未知值，預設為隱藏文字欄位
        if choice is None:
            return gr.update(visible=False)

        choice_str = str(choice).strip()
        if choice_str == "短文模式":
            # 設為 2 行，並顯示
            return gr.update(lines=2, visible=True, label="短文寫作")
        elif choice_str == "長文模式":
            # 設為 8 行，並顯示
            return gr.update(lines=8, visible=True, label="長文寫作")
        else:
            # 隱藏文字欄位
            return gr.update(visible=False)

# 啟動 Gradio 應用（若要分享可設定 share=True）
demo.launch()