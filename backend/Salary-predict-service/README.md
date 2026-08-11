# Salary 薪資預測服務

這是一個以 FastAPI 建立的薪資預測服務，示範如何將資料前處理、模型訓練與序列化流程整合成可部署的服務。

## 功能

- 💰 依據工作年資、教育程度與城市，預測薪資水準
- 🧠 支援線上重新訓練模型，並即時更新服務使用的模型
- 📦 會將模型與前處理器序列化成 joblib 檔案，方便後續部署或重複使用
- 🧾 `Salary_Data2.csv` 中的 Salary 欄位為每月薪資（單位：千元），本服務回傳結果會轉換成實際新臺幣元 (NT$)

## 專案結構

| 檔案 | 說明 |
|---|---|
| app.py | FastAPI 服務主程式 |
| train_save.py | 訓練與儲存薪資預測模型 |
| salary_model.joblib | 已訓練好的薪資模型 |
| iris_model.joblib | 另外提供的 Iris 範例模型檔 |
| requirements.txt | 依賴套件清單 |

## 本地執行

```bash
pip install -r requirements.txt
python app.py
```

啟動後可使用：

- Swagger UI: http://localhost:8000/docs
- 主要 API: http://localhost:8000/predict

## API 範例

### 預測薪資

POST /predict

```json
{
  "years_experience": 5,
  "education_level": "大學",
  "city": "城市A"
}
```

### 重新訓練模型

POST /train

```json
{
  "test_size": 0.2,
  "random_state": 76,
  "model_type": "LinearRegression",
  "alpha": 1.0
}
```

## 重新訓練

```bash
python train_save.py
```

若模型檔不存在，服務啟動時也會自動重新訓練。