"""backend/08_07/app.py

簡要說明:
    FastAPI 服務，用於訓練、儲存與載入薪資預測模型。
    - 提供 `/train` POST 端點以線上重新訓練模型並即時更新服務使用的模型狀態。
    - 模型訓練與序列化由 `train_save.train_and_save_model` 處理，序列化結果以 `joblib` 儲存。

主要變數說明:
    - `MODEL_STATE`: 服務運行時的模型快取，包含模型物件、編碼器、標準化器與特徵資訊等。
    - `model_path`: 序列化模型檔案路徑（salary_model.joblib）。

所有註解與說明均以繁體中文撰寫，方便維護與使用者理解。
"""

import os
import sys
from typing import Optional

from pydantic import BaseModel, Field
import joblib
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import uvicorn

from train_save import train_and_save_model


current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

model_path = os.path.join(current_dir, "salary_model.joblib")
# 全域狀態快取：在服務啟動或重新訓練後會更新
MODEL_STATE = {}


class TrainConfig(BaseModel):
    """Pydantic 輸入驗證模型，用於 `/train` 端點的 request body。"""
    test_size: float = Field(0.2, description="測試集分割比例", ge=0.1, le=0.5)
    random_state: int = Field(76, description="隨機種子", ge=0)
    model_type: str = Field("LinearRegression", description="模型演算法類型 (LinearRegression, Lasso, Ridge)")
    alpha: float = Field(1.0, description="正則化強度 alpha (適用於 Lasso 與 Ridge)", ge=0.001, le=100.0)

class TrainResult(BaseModel):
    """Pydantic 回應模型，用於 `/train` 端點的 response body。

    欄位:
        - status: 執行結果狀態 (e.g., "success")
        - r2: 測試集 R^2 決定係數
        - coef: 模型係數列表
        - intercept: 截距
        - feature_coefs: 特徵名稱對應係數的字典
        - model_type / alpha: 訓練時使用的模型類型與正則化參數
        - train_time: 訓練耗時（秒）
        - message: 額外提示訊息
    """
    status: str = Field(..., description="執行結果狀態")
    r2: float = Field(..., description="測試集 R-squared 決定係數")
    coef: list[float] = Field(..., description="特徵權重係數列表")
    intercept: float = Field(..., description="截距")
    feature_coefs: dict[str, float] = Field(..., description="特徵及其權重映射")
    model_type: str = Field(..., description="模型演算法類型")
    alpha: float = Field(..., description="正則化強度 alpha")
    train_time: float = Field(..., description="訓練耗時 (秒)")
    message: str = Field(..., description="提示訊息")

class SalaryInput(BaseModel):
    years_experience: float = Field(..., ge=0.0, le=50.0)
    education_level: str
    city: str

class SalaryOutput(BaseModel):
    predicted_salary: float
    estimated_annual_salary: float


def load_model_state():
    """從序列化檔案載入模型狀態到 `MODEL_STATE`。

    行為:
        - 若模型檔案不存在，呼叫 `train_and_save_model()` 以產生預設模型檔案。
        - 使用 `joblib.load` 載入模型檔案，並將必要物件更新到 `MODEL_STATE`。
    """
    global MODEL_STATE
    # 若模型檔不存在，先觸發一次訓練以建立模型檔
    if not os.path.exists(model_path):
        train_and_save_model()

    model_data = joblib.load(model_path)
    # 清除並更新全域快取，方便其它 endpoint 或函式讀取
    MODEL_STATE.clear()
    MODEL_STATE.update(
        {
            "model": model_data.get("model"),
            "oe": model_data.get("oe"),
            "ohe": model_data.get("ohe"),
            "scaler": model_data.get("scaler"),
            "r2": model_data.get("r2"),
            "feature_names": model_data.get("feature_names"),
            "feature_coefs": model_data.get("feature_coefs", {}),
            "model_type": model_data.get("model_type"),
            "alpha": model_data.get("alpha"),
        }
    )

load_model_state()

app = FastAPI()

origins = [
    "http://localhost:4173",
    "http://127.0.0.1:4173",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://sallryxin-zi-yu-ce.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.post("/train", response_model=TrainResult)
def train_endpoint(config:TrainConfig):
    """
    訓練端點：傳入測試集比例、隨機種子、模型類型與 alpha，線上重新訓練模型，並即時更新服務所使用的模型。
    """
    try:
        # 1. 執行重新訓練並儲存模型
        res = train_and_save_model(
            test_size=config.test_size,
            random_state= config.random_state,
            model_type= config.model_type,
            alpha=config.alpha
        )
         # 2. 線上重新載入最新模型狀態至全域變數
        load_model_state()
    except Exception as e:
        # 捕捉所有例外並回傳 500 與錯誤訊息，方便前端或使用者了解失敗原因
        raise HTTPException(status_code=500, detail=f"線上訓練失敗: {str(e)}")

    return res

@app.post("/predict", response_model=SalaryOutput)
def predict_endpoint(payload:SalaryInput):
    oe = MODEL_STATE["oe"]
    ohe = MODEL_STATE["ohe"]
    scaler = MODEL_STATE["scaler"]
    model = MODEL_STATE["model"]

    edu_encoded = int(oe.transform(pd.DataFrame([[payload.education_level]], columns=["EducationLevel"]))[0][0])
    city_vector = ohe.transform(pd.DataFrame([[payload.city]], columns=["City"]))
    city_cols = ohe.get_feature_names_out(['City'])
    feature_row = [payload.years_experience, edu_encoded] + list(city_vector[0])
    features = pd.DataFrame([feature_row],columns=["YearsExperience", "EducationLevel"] + list(city_cols))
    X_scaled = scaler.transform(features)
    predicted_salary_thousands = float(model.predict(X_scaled)[0])
    # Salary_Data2.csv 中的 Salary 欄位為每月薪資（千元）。
    # 這裡回傳實際新臺幣元 (NT$) 的月薪與 14 個月年薪估算。
    predicted_salary = predicted_salary_thousands * 1000.0
    return SalaryOutput(
        predicted_salary=predicted_salary,
        estimated_annual_salary=predicted_salary * 14.0
    )


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)