import gradio as gr

# 全域變數：所有使用者共享同一份 scores 清單
# 注意：這表示不同瀏覽器分頁或不同使用者的分數會互相影響
scores = []

# track_score 函式：將使用者輸入的分數加入全域排行榜
# 1. 將新分數加入 scores 清單
# 2. 將分數依照大小排序
# 3. 取出前三名並回傳給介面顯示
def track_score(score):
    scores.append(score)
    top_scores = sorted(scores, reverse=True)[:3]
    return top_scores

# 建立 Gradio 介面
# inputs: 輸入元件為數字欄位，標示為「您的分數」
# outputs: 輸出元件為 JSON 格式，用於顯示前 3 名分數排行榜
# title: 介面標題
# description: 介面說明文字，提示使用者可開啟多個分頁測試共享狀態

demo = gr.Interface(
    inputs=gr.Number(label="您的分數"),
    outputs=gr.JSON(label="前 3 名最高分數排行榜"),
    fn=track_score,
    title="🏆 全域分數排行榜",
    description="請輸入您的分數！本系統會追蹤所有使用者的前 3 名最高分數。請開啟多個瀏覽器分頁同時測試，觀察資料如何共享。",
)

# 啟動 Gradio 介面，並設定 share=True 以便生成公開連結給其他人測試
demo.launch(share=True)