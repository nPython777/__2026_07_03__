"""
practice5.py

範例說明：
示範如何將一個函式的回傳值分別輸出到多個 Gradio 元件（回傳 list/tuple 對應多個 outputs）。
此範例模擬「餵食」動作：
- `food_box` 保存剩餘食物數量（整數）；按下「餵食」後，若有食物則數量減 1，並在 `status_box` 顯示寵物狀態。

快速使用：
1. 安裝 Gradio：`pip install gradio`
2. 執行：`python practice5.py`
3. 在本機頁面操作 `餵食` 按鈕測試行為。

注意事項：
- 函式包含簡單輸入檢查（處理 None 及非數值情況），並確保數量不會成為負值。
"""

import gradio as gr

with gr.Blocks() as demo:
    # 數值元件：剩餘食物數量，初始值為 5
    # 可加上參數如 `precision=0` 或 `step=1` 強制整數步進，但此處保留預設
    food_box = gr.Number(value=5, label="剩餘食物數量")

    # 文字輸出元件：顯示寵物狀態（飽足/飢餓）
    status_box = gr.Textbox(label="寵物狀態")

    @gr.Button("餵食").click(inputs=food_box, outputs=[food_box, status_box])
    def eat(food):
        """按下餵食按鈕時呼叫。

        參數:
            food: 來自 `food_box` 的目前值（可能為 None 或非數值）。

        回傳:
            tuple: (新的 food 值, 狀態字串)
        """
        # 檢查輸入是否為有效數值
        if food is None:
            return 0, "請先設定剩餘食物數量。"

        try:
            # 嘗試將輸入轉為數字並做邏輯判斷
            num = float(food)
        except Exception:
            return 0, "食物數量格式不正確，請輸入數字。"

        # 以整數計算剩餘數量
        num_int = int(num)
        if num_int > 0:
            return num_int - 1, "飽足 😋"
        else:
            # 保持數量為 0，並回傳飢餓狀態
            return 0, "飢餓 😢"

# 啟動 Gradio 應用
demo.launch()