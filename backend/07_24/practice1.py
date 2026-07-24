import gradio as gr

# 定義函式 greet，接收使用者姓名與強度數值
# 回傳 Hello 訊息，並根據 intensity 參數產生對應數量的驚嘆號
def greet(name, intensity):
    return "Hello," + name + "!" * int(intensity)

# 建立 Gradio 介面物件
# fn: 使用者送出資料後要執行的函式
# inputs: 介面輸入元件類型，文字輸入與滑桿
# outputs: 輸出結果類型，這裡只顯示文字
# examples: 預設展示的範例資料，方便使用者快速測試
demo = gr.Interface(
    fn=greet,
    inputs=["text", "slider"],
    outputs=["text"],
    examples=[
        ["鐵拳無敵孫中山", 3],
        ["南拳北腿蔣中正", 2]
    ]
)

# 啟動介面，預設會在本機開啟瀏覽器頁面
demo.launch()