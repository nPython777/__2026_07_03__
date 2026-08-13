# PRD：Python 連結 Render Postgres 教學文件（python連結postgres.md）

## 1. 產品概述

### 1.1 產品名稱
「Python 連結 Render Postgres 教學文件」

### 1.2 產品定位
這是一份**給學生的教學文件**，教導學生如何使用 Python 連接到雲端 Render 平台上的 PostgreSQL 資料庫，並透過 `.env` 檔案隱藏與保護資料庫密碼。

### 1.3 產出檔案
- 主要產出檔案名稱：**`python連結postgres.md`**
- 檔案位置：與本 PRD 相同資料夾（`backend/08_13/`）
- 檔案格式：Markdown（`.md`）
- 撰寫語言：繁體中文

### 1.4 目標對象（Target Audience）
- **學生**：具備基礎 Python 語法能力，對資料庫不熟悉或僅接觸過 SQLite 的初學者。
- 學生應已經了解：變數、函式、`pip` 安裝套件、基本的 `try/except` 錯誤處理概念。
- 學生**不需要**具備：雲端平台經驗、PostgreSQL 管理經驗、環境變數概念。

### 1.5 使用情境
學生正在學習「雲端資料庫」的應用，想要：
1. 在 Render 免費方案上建立一個 PostgreSQL 資料庫。
2. 從本機的 Python 程式（例如 Jupyter Notebook、`.py` 腳本）連上這個資料庫。
3. 建立資料表、新增資料、查詢資料。
4. 學會不要把密碼直接寫在程式碼裡，而是用 `.env` 保護。

## 2. 背景與動機

- Render 提供免費的 PostgreSQL 雲端資料庫，很適合學生練習，且不需要安裝本機資料庫伺服器。
- 學生的資料庫連線資訊包含 `host`、`port`、`database`、`user`、`password`，其中 **password 是敏感資料**。
- 若把密碼直接寫在 Python 程式碼或 Notebook 中，容易在分享程式碼時**外洩密碼**。
- 因此需要教導學生使用 `.env` 檔案 + `python-dotenv` 套件，把密碼放在 `.env` 中，並透過 `.gitignore` 避免上傳到 GitHub。

## 3. 產品範圍（Scope）

### 3.1 教學文件必須涵蓋的內容

#### 3.1.1 前置準備
- 註冊 Render 帳號（render.com）。
- 建立 PostgreSQL 資料庫（Free instance）。
- 取得 Render 提供的 **Internal Database URL / External Database URL**。
- 說明何謂「連線字串（Connection String）」。

#### 3.1.2 Python 環境準備
- 建立專案資料夾（例如 `backend/08_13/`）。
- 使用 `uv` 建立虛擬環境並啟用。
- 安裝所需套件：
  - `psycopg2-binary` 或 `psycopg[binary]`（PostgreSQL 連線驅動）
  - `python-dotenv`（讀取 `.env` 檔案）
- 需要寫出明確的指令，例如：
  - `uv init` / `uv add psycopg2-binary python-dotenv`
  - 或 `pip install psycopg2-binary python-dotenv`

#### 3.1.3 使用 `.env` 保護密碼（重點章節）
- 建立 `.env` 檔案，內容範例：
  ```
  DATABASE_URL=postgresql://user:password@host:5432/dbname
  ```
  或拆開成多個變數：
  ```
  PGHOST=your-db-host.render.com
  PGPORT=5432
  PGUSER=db_user
  PGPASSWORD=your_password
  PGDATABASE=db_name
  ```
- 說明 `.env` 的作用與原理（純文字檔，存放環境變數）。
- **重要提醒**：`.env` 內含機密，不可以直接寫在程式碼裡。
- 建立 `.gitignore`，內容包含 `.env`，避免上傳 GitHub。
- 建立 `.env.example` 範例檔（只放欄位不放真實密碼），方便分享給他人參考格式。
- 警告：**不要**把 `.env`、真實密碼貼到聊天室、作業繳交、或 GitHub 上。

#### 3.1.4 撰寫連線程式碼
- 在 Python 中載入 `.env`：`from dotenv import load_dotenv` + `load_dotenv()`。
- 從環境變數讀取連線資訊：`os.getenv("DATABASE_URL")`。
- 使用 `psycopg2.connect()` 建立連線。
- 建立 cursor、執行 SQL、`commit()`、關閉連線（cursor / connection）。
- 使用 `try/except` 與 `finally` 處理連線失敗與資源釋放。
- 提供至少兩個完整範例：
  1. 查詢版：連線後執行 `SELECT version();` 或建立資料表。
  2. 寫入版：建立資料表並 `INSERT` 一筆資料後查詢回來。

#### 3.1.5 驗證與除錯
- 常見錯誤整理與解法：
  - `OperationalError: connection failed`（主機/連線字串錯誤、IP 未授權）
  - `password authentication failed`（密碼錯誤）
  - 憑證 / SSL 問題（Render 免費版需要 SSL，`sslmode=require`）
  - 套件未安裝（`ModuleNotFoundError: No module named 'psycopg2'`）
- 告訴學生如何確認連線成功（例如 print 出 Postgres 版本）。

### 3.2 非目標（Out of Scope）
- 不教 PostgreSQL 完整的 SQL 語法教學（只涵蓋 CRUD 基本操作）。
- 不涵蓋 Render 付費方案、高可用性、備份等進階功能。
- 不涵蓋前端網頁串接資料庫。
- 不涵蓋 FastAPI / Flask 整合（這是後續章節）。

## 4. 教學文件結構建議（章節大綱）

`python連結postgres.md` 建議章節如下：

1. **前言**：為什麼要用雲端資料庫、為什麼要保護密碼。
2. **Step 1：在 Render 建立 PostgreSQL 資料庫**（含 UI 操作步驟說明、取得連線字串的位置）。
3. **Step 2：準備 Python 環境**（uv 虛擬環境、安裝套件）。
4. **Step 3：用 `.env` 藏好密碼**（建立 `.env`、`.env.example`、`.gitignore`）。
5. **Step 4：撰寫連線程式**（完整可執行程式碼範例）。
6. **Step 5：實作練習**（給學生練手的任務：建資料表、新增資料、查詢資料）。
7. **常見問題（FAQ）與除錯**。
8. **安全提醒總結**。

## 5. 內容詳細度要求（給執行模型的指示）

由於此 PRD 是給**其他模型**執行用，請遵守以下詳細度要求：

### 5.1 程式碼範例要求
- 每個範例都必須是**可以直接複製執行**的完整程式碼（包含 `import`、`load_dotenv()`、`try/except`）。
- 程式碼必須標註對應的程式語言（```python）。
- 每個程式碼區塊前要有**一步步的中文說明**，解釋每一段在做什麼。
- 需同時提供「用 `DATABASE_URL` 單一變數」與「拆開多個變數（PGHOST / PGPORT / PGUSER / PGPASSWORD / PGDATABASE）」兩種讀法。

### 5.2 `.env` 章節要求
- 要明確示範 `.env` 檔案的內容。
- 要示範 `.gitignore` 的內容（至少包含 `.env`、`.env.*`、`__pycache__/`、`.venv/`、`.ipynb_checkpoints/`）。
- 要示範 `.env.example` 的內容（使用假值，例如 `PGPASSWORD=your_password_here`）。
- 要有一份「密碼安全注意事項」清單。

### 5.3 語氣與排版要求
- 全程使用**繁體中文**。
- 語氣要**親切、淺白**，像老師在帶學生一步步操作。
- 每個步驟都要有**小標題**，並在步驟前說明「這個步驟做完，你會得到什麼結果」。
- 善用表格整理：套件清單、連線參數對照表、常見錯誤對照表。
- 章節之間的順序要能讓學生**照著做就能成功**。

### 5.4 執行模型必須完成的最終產出
- 在 `backend/08_13/python連結postgres.md` 產生完整教學文件。
- 可視需要於 `backend/08_13/` 一併建立 `.env.example` 與 `.gitignore` 示範檔。
- **不得**建立包含真實密碼的任何檔案。

## 6. 成功驗收標準（Acceptance Criteria）

- [ ] `backend/08_13/python連結postgres.md` 存在，且為完整繁體中文教學文件。
- [ ] 文件包含：Render 建庫步驟、環境準備、`.env` 教學、`.gitignore` 教學、完整連線程式碼範例。
- [ ] 文件包含至少一個可執行的「連線成功驗證」範例（如查詢 Postgres 版本）。
- [ ] 文件包含常見錯誤與解法。
- [ ] 文件明確警告密碼不要寫在程式碼或上傳 GitHub。
- [ ] 程式碼範例皆使用 `.env` 讀取敏感資訊，沒有任何硬編碼密碼。

## 7. 參考資源

- Render 官方文件：PostgreSQL（需由執行模型自行查證最新步驟）
- psycopg2 官方文件
- python-dotenv 官方文件
- 本專案既有 `RENDER_DEPLOY.md`（位於 repo 根目錄）可參考 Render 部署相關慣例
