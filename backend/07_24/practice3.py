import gradio as gr

# 定義函式 store_message，處理單次訊息提交與會話歷史
# message: 使用者輸入的文字
# history: 會話狀態清單，用於儲存該分頁的歷史訊息
# 回傳值包含要顯示的輸出資料與更新後的 history
def store_message(message: str, history: list[str]):
    output = {
        "目前訊息": message,
        "歷史訊息(倒序展示)": history[::-1]
    }
    # 將目前訊息存入 history，保留會話中的歷史紀錄
    history.append(message)
    return output, history

# 建立 Gradio 介面
# inputs:
#   1. Textbox: 用戶輸入訊息
#   2. State: 會話狀態變數，用來儲存當前分頁的歷史訊息清單
# outputs:
#   1. JSON: 顯示目前訊息與倒序的歷史訊息列表
#   2. State: 回傳更新後的會話狀態，讓 Gradio 保留下一次呼叫時的歷史資料
# fn: 使用者送出資料後要呼叫的函式
# title: 介面標題
# description: 說明此介面使用會話狀態，且資料只存在於當前分頁

demo = gr.Interface(
    inputs=[
        gr.Textbox(label="請輸入您的訊息", placeholder="在此輸入文字..."),
        gr.State(value=[])
    ],
    outputs=[
        gr.JSON(label="訊息日誌"),
        gr.State()
    ],
    fn=store_message,
    title="💬 個人歷史訊息記錄器",
    description="您在此分頁輸入的每一筆訊息都會被暫存在會話狀態中，其他連線的使用者不會看到您的資料。"
)

# 啟動 Gradio 介面，預設在本機啟動網頁服務
demo.launch()