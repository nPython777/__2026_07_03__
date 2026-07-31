"""
practice4.py

示範如何在單一 Gradio Blocks 應用中配置多個數值元件與按鈕，每個按鈕觸發獨立的資料傳遞路徑。

功能說明：
- 有兩個數值欄位 `A` 與 `B`。
- 按鈕 `將 A 的值加 1 後填入 B`：讀取 A 的數值，加 1 後將結果寫回 B。
- 按鈕 `將 B 的值加 1 後填入 A`：讀取 B 的數值，加 1 後將結果寫回 A。

快速上手：
1. 安裝 Gradio：`pip install gradio`
2. 執行：`python practice4.py`，開啟輸出網址後即可互動。

注意：此範例保留原本的行為，但加入輸入檢查以避免 None 值或非數值錯誤。
"""

import gradio as gr

with gr.Blocks() as demo:
    # 數值輸入元件：A 與 B
    a = gr.Number(label="數值A")
    b = gr.Number(label="數值B")

    # 兩個按鈕分別負責把另一個欄位的數值 +1 並寫入目標欄位
    atob = gr.Button("將 A 的值加 1 後填入 B")
    btoa = gr.Button("將 B 的值加 1 後填入 A")

    @atob.click(inputs=a, outputs=b)
    def a_to_b(val_a):
        """讀取 A 的值並回傳 A+1 作為 B 的新值。

        參數:
            val_a (float|int|None): 來自欄位 A 的數值，可能為 None。

        回傳:
            float|str: 若輸入有效回傳數值；若為 None 或非數值則回傳提示字串。
        """
        if val_a is None:
            return "請先在 A 欄位輸入數值。"
        try:
            return val_a + 1
        except Exception:
            return "A 欄位數值無法計算，請輸入數字。"

    @btoa.click(inputs=b, outputs=a)
    def b_to_a(val_b):
        """讀取 B 的值並回傳 B+1 作為 A 的新值。

        參數與回傳同上。
        """
        if val_b is None:
            return "請先在 B 欄位輸入數值。"
        try:
            return val_b + 1
        except Exception:
            return "B 欄位數值無法計算，請輸入數字。"

# 啟動應用
demo.launch()