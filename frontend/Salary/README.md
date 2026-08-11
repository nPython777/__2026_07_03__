# Salary 薪資預測前端

這是 `frontend/Salary` 的 React + TypeScript + Vite 前端專案，提供與 `backend/Salary-predict-service` 互動的使用者介面。

本前端預測結果會自動將後端模型輸出由「每月薪資千元」轉換為實際新臺幣元 (NT$)，並顯示月薪與年薪估算。

## 功能

- 💰 依據工作年資、教育程度與城市輸入資料，呼叫後端 `/predict` 取得薪資預測
- ⚙️ 提供模型訓練頁面，呼叫後端 `/train` 重新訓練 Salary 模型
- 🎨 參考 `frontend/iris` 的 UI 風格與專案架構

## 啟動方式

```bash
cd frontend/Salary
npm install
npm run dev
```

預設會連線到 `http://localhost:8000`，如果你要切換後端位置，可新增環境變數：

```bash
VITE_API_BASE=http://localhost:8000 npm run dev
```

## 檔案說明

- `src/App.tsx`：主應用程式入口
- `src/api.ts`：與 Salary-predict-service 的 API 溝通
- `src/components/PredictTab.tsx`：薪資預測頁面
- `src/components/TrainTab.tsx`：模型訓練頁面
- `src/components/Slider.tsx`：共用滑桿元件
- `index.html`、`vite.config.ts`、`tsconfig*.json`：前端建置設定

## 注意

請先啟動 `backend/Salary-predict-service`，讓前端能正常呼叫預測與訓練端點。