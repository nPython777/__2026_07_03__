# Render 部署指南

此專案包含兩個獨立服務：

1. `backend/Salary-predict-service`：FastAPI 後端服務
2. `frontend/Salary`：React + Vite 前端靜態站點

## 1. 將專案推到 GitHub

Render 會直接從 GitHub 倉庫拉取。請先將此專案推送到你的 GitHub repository。

## 2. 使用 Render Web Service 部署後端

在 Render 中新增一個 Web Service：

- Service type: `Web Service`
- Environment: `Python`
- Root directory: `backend/Salary-predict-service`
- Build Command:
  ```bash
  pip install -r requirements.txt
  ```
- Start Command:
  ```bash
  uvicorn app:app --host 0.0.0.0 --port $PORT
  ```

### 注意

- `render.yaml` 中已設定後端服務的啟動方式。
- 若後端服務啟動失敗，可先確認 `requirements.txt` 是否正確安裝。

## 3. 使用 Render Static Site 部署前端

在 Render 中新增一個 Static Site：

- Service type: `Static Site`
- Root directory: `frontend/Salary`
- Build Command:
  ```bash
  npm install && npm run build
  ```
- Publish Directory: `dist`

## 4. 設定前端環境變數

前端會讀取 `VITE_API_BASE`，用來指定後端 API URL。請在 Render UI 或 `render.yaml` 中設定：

- `VITE_API_BASE=https://<你的後端服務域名>`

例如：

- `VITE_API_BASE=https://salary-backend.onrender.com`

如果沒有設定，前端預設會連到 `http://localhost:8000`，在 Render 上會失敗。

## 5. render.yaml 自動建立服務

本專案已包含 `render.yaml`，可讓 Render 自動識別以下服務：

- `salary-backend`
- `salary-frontend`

如果你使用 Render 的 `Connect Repository`，Render 會自動讀取 `render.yaml` 並建立這兩個服務。

## 6. 建議部署流程

1. 將 repo push 到 GitHub。
2. 在 Render 裡新增 `salary-backend` 與 `salary-frontend` 服務，或直接用 `render.yaml`。
3. 設定 `VITE_API_BASE` 為後端提供的公開 URL。
4. 等待 build 與 deploy 成功。
5. 測試前端頁面是否能呼叫後端 `/predict`。

## 7. 常見問題

- **前端載入但預測失敗**：通常是 `VITE_API_BASE` 未正確配置。
- **後端 500 錯誤**：請檢查後端 `requirements.txt` 是否安裝完成，且 `Salary_Data2.csv` 與 `salary_model.joblib` 能正常存取。
- **Render 未自動部署**：可在 Render UI 裡手動新增服務並設定 root 位置。
