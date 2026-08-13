# Python 連結 Render Postgres 教學

> 給學生的完整教學文件：如何用 Python 連上雲端 Render 平台上的 PostgreSQL 資料庫，並學會用 `.env` 保護你的密碼。

---

## 前言：為什麼要學這個？

寫程式的時候，資料都存放在哪裡呢？你可能用過 Excel、用過 SQLite，但這些資料一直以來都存在「你個人的電腦」裡。這堂課，我們要把資料搬到**雲端**，讓任何人透過網路就能存取，也能讓你的網站（例如 FastAPI）讀取同一份資料。

[Render](https://render.com) 是一個雲端平台，提供免費的 **PostgreSQL 雲端資料庫**。PostgreSQL（簡稱 Postgres）功能非常強大，也是業界廣泛使用的資料庫之一。

**但是，這裡有一個很關鍵的問題**：資料庫的密碼是你最重要的秘密。如果把密碼直接寫在程式碼裡，當你把程式碼分享出去、上傳到 GitHub、或交給老師時，**密碼就跟著外洩了**！

所以，這份教學會教你兩件事：

1. 如何用 Python 連到 Render 上的 PostgreSQL。
2. 如何用 `.env` 檔案把密碼藏起來，讓密碼永遠不出現在程式碼中。

---

## Step 1：在 Render 建立 PostgreSQL 資料庫

> 這個步驟做完，你會拿到一串「連線字串」，它是連到雲端資料庫的鑰匙。

### 1.1 註冊 Render 帳號

1. 打開瀏覽器，進入 <https://render.com>。
2. 點右上角 **Sign Up**，可以用 GitHub 或 Google 帳號快速註冊。
3. 註冊完成後，Render 會引導你進行帳號設定（可能需要驗證 Email 或手機號碼）。

> 注意：Render 的免費方案政策可能會調整，一切以官網當下顯示為準。學生通常可以申請免費額度。

### 1.2 建立 PostgreSQL 資料庫

1. 登入後，點右上角 **New +**，選擇 **PostgreSQL**。
2. 設定資料庫名稱（Name），例如 `student-db`。
3. 選擇 **Free** 方案（如果有免費選項可選）。
4. 按下 **Create Database**，等 Render 建立完成（約需 1 分鐘）。

### 1.3 找到你的「連線字串」

建立完成後，畫面會進入資料庫的詳細頁面，你可以在上面看到以下資訊：

| 欄位 | 說明 | 範例 |
|------|------|------|
| **Internal Database URL** | 給「也在 Render 上」的服務用的連線網址 | `postgresql://user:xxx@host:5432/dbname` |
| **External Database URL** | 給「你的電腦（本機）」用的連線網址 | `postgresql://user:xxx@host:5432/dbname` |
| **Hostname** | 資料庫主機位置 | `dpg-xxxxxxx-a.oregon-postgres.render.com` |
| **Port** | 連線埠號 | `5432` |
| **Database** | 資料庫名稱 | `student_db` |
| **User** | 使用者名稱 | `student_user` |
| **Password** | 密碼（超級重要！） | `xxxxx` |

> 💡 **重點**：你的 Python 程式是在「你自己電腦」上跑的，所以要使用 **External Database URL**。它是包含帳號密碼的完整網址，長得像這樣：
>
> `postgresql://student_user:你的密碼@dpg-xxxx.oregon-postgres.render.com:5432/student_db`

### 1.4 什麼是「連線字串」？

連線字串（Connection String）就是把「連到資料庫要用的所有資訊」打包成的一串文字，格式如下：

```
postgresql://使用者名稱:密碼@主機位置:埠號/資料庫名稱
```

把它拆開來看，會更清楚：

| 部分 | 位置 | 意思 |
|------|------|------|
| `postgresql://` | 開頭 | 資料庫類型是 PostgreSQL |
| `student_user` | 使用者名稱 | 登入資料庫的帳號 |
| `你的密碼` | 密碼 | 登入資料庫的鑰匙（秘密！） |
| `dpg-xxxx...render.com` | 主機位置 | 資料庫住在哪裡 |
| `5432` | 埠號 | PostgreSQL 預設的連接埠 |
| `student_db` | 資料庫名稱 | 要使用的資料庫 |

---

## Step 2：準備 Python 環境

> 這個步驟做完，你的電腦上就會有 Python 連資料庫需要的「工具」。

### 2.1 建立專案資料夾

請建立一個專案資料夾，例如：

```
backend/08_13/
```

接下來的所有檔案都會放在這個資料夾裡。

### 2.2 用 uv 建立虛擬環境

本專案使用 **uv** 管理 Python 環境。虛擬環境就像是每個專案的「獨立小房間」，讓不同專案可以各自安裝不同版本的套件，彼此不會互相干擾。

首先，建立專案。在終端機（PowerShell）中輸入：

```bash
uv init
```

接著建立虛擬環境：

```bash
uv venv
```

然後啟動虛擬環境（Windows PowerShell）：

```bash
.venv\Scripts\activate
```

如果命令列最前面出現 `(.venv)`，代表虛擬環境啟用成功！

> 小提醒：其實 `uv add` 安裝套件時也會自動建立虛擬環境，這裡先手動建立，是為了讓步驟更清楚。
>
> 如果你沒有 uv，也可以改用傳統方式：

```bash
pip install psycopg2-binary python-dotenv
```

### 2.3 安裝需要的套件

虛擬環境啟用後，安裝兩個套件：

```bash
uv add psycopg2-binary python-dotenv
```

| 套件 | 用途 |
|------|------|
| `psycopg2-binary` | 讓 Python 能跟 PostgreSQL 對話的「驅動程式」 |
| `python-dotenv` | 讓 Python 能讀取 `.env` 檔案裡的環境變數 |

安裝完成後，輸入以下指令確認安裝成功：

```bash
uv pip list
```

應該會看到 `psycopg2-binary` 與 `python-dotenv`。

---

## Step 3：用 `.env` 藏好密碼（本教學最重要的章節！）

> 這個步驟做完，你的密碼會被藏進 `.env` 檔案裡，不會出現在程式碼中。

### 3.1 為什麼不能把密碼寫在程式碼裡？

先來看看常見的錯誤寫法：

```python
# ❌ 錯誤示範：不要把密碼直接寫在程式碼裡！
conn = psycopg2.connect(
    host="dpg-xxxx.oregon-postgres.render.com",
    database="student_db",
    user="student_user",
    password="這是我的密碼1234",  # ❌ 危險！
    port="5432"
)
```

如果照這樣寫，你的密碼就會跟著程式碼一起被分享出去。只要有人拿到你的程式碼，就等於拿到你資料庫的鑰匙，可以偷看、甚至刪除你的資料！

**正確做法**：把密碼放進一個叫 `.env` 的檔案，讓程式碼自己去讀取它。

### 3.2 建立 `.env` 檔案

在專案資料夾 `backend/08_13/` 中，建立一個名為 `.env` 的檔案（注意：開頭有一個點，不要打錯）。

`.env` 檔案的內容如下：

```
DATABASE_URL=postgresql://student_user:你的密碼@dpg-xxxx.oregon-postgres.render.com:5432/student_db
```

也可以把資訊拆開，寫成多行：

```
PGHOST=dpg-xxxx.oregon-postgres.render.com
PGPORT=5432
PGUSER=student_user
PGPASSWORD=你的密碼
PGDATABASE=student_db
```

> 兩種寫法都可以，選一種就好。第 4 章會教你如何在 Python 中讀取。
>
> ⚠️ **請務必**把 `你的密碼` 換成 Render 上顯示的真實密碼。

#### `.env` 的運作原理

`.env` 只是一個純文字檔案，專門用來存放「環境變數」。Python 透過 `python-dotenv` 套件讀取它，把內容變成 Python 可以讀取的變數。因為這個檔案不屬於程式碼，所以它**不會**跟著程式碼一起被分享出去。

### 3.3 建立 `.env.example` 範例檔

`.env.example` 是給別人看的「範本」，內容只有欄位名稱和假值，**絕對不放真實密碼**。別人複製你的專案時，可以照著它建立自己的 `.env`。

建立 `backend/08_13/.env.example`，內容如下：

```
# 請複製這個檔案並改名為 .env
# 然後把你的真實連線資訊填進去！
DATABASE_URL=postgresql://user:your_password_here@host.render.com:5432/your_dbname
```

或拆開版：

```
PGHOST=your-host.render.com
PGPORT=5432
PGUSER=your_username
PGPASSWORD=your_password_here
PGDATABASE=your_dbname
```

> `.env.example` 可以放心上傳 GitHub，因為裡面沒有真實密碼。

### 3.4 建立 `.gitignore` 保護 `.env`

如果你會把專案上傳到 GitHub，**一定要**建立 `.gitignore` 檔案，告訴 Git「不要上傳 .env」。

建立 `backend/08_13/.gitignore`，內容如下：

```
# 環境變數檔（含密碼，絕對不能上傳！）
.env
.env.*
!.env.example

# Python
__pycache__/
*.pyc
.ipynb_checkpoints/
.venv/
venv/
```

各行的意思：

- `.env` → 忽略，不上傳。
- `.env.*` → 忽略所有以 `.env.` 開頭的檔案（例如 `.env.local`）。
- `!.env.example` → 例外規則，`.env.example` 要上傳（因為沒有密碼，可以當範本）。

> 💡 上傳 GitHub 前，請再檢查一次：**Repository 裡絕對不能有 `.env` 檔案**！

### 3.5 密碼安全注意事項（請仔細閱讀！）

- 🔴 **絕對不要**把 `.env` 檔案上傳到 GitHub。
- 🔴 **絕對不要**把密碼寫在程式碼或 Jupyter Notebook 裡。
- 🔴 **絕對不要**把 `.env` 內容或密碼貼到聊天室、LINE、作業繳交區。
- 🟢 分享專案時，只分享 `.env.example` 這種沒有密碼的範本。
- 🟢 如果懷疑密碼外洩，請立刻到 Render 上**重設密碼**。

---

## Step 4：撰寫連線程式

> 這個步驟做完，你會寫出一個能成功連到雲端資料庫的 Python 程式。

### 4.1 方法一：使用單一 `DATABASE_URL`（推薦，最簡單）

在專案資料夾建立 `connect_db.py`，內容如下：

```python
import os
import psycopg2
from dotenv import load_dotenv

# 1. 讀取 .env 檔案，把裡面的變數載入到環境變數中
load_dotenv()

# 2. 從環境變數取得連線字串
DATABASE_URL = os.getenv("DATABASE_URL")

try:
    # 3. 建立與資料庫的連線
    conn = psycopg2.connect(DATABASE_URL)

    # 4. 建立 cursor（類似「游標」，用來執行 SQL）
    cur = conn.cursor()

    # 5. 執行 SQL：查詢 PostgreSQL 版本
    cur.execute("SELECT version();")

    # 6. 取得查詢結果並顯示
    version = cur.fetchone()
    print("✅ 連線成功！PostgreSQL 版本：", version[0])

    # 7. 關閉 cursor 與連線（用完一定要關！）
    cur.close()
    conn.close()

except Exception as e:
    # 8. 連線失敗時，把錯誤印出來給我們看
    print("❌ 連線失敗：", e)
```

**一步步解說**（對應程式碼中的註解編號）：

| 編號 | 在做什麼 |
|------|----------|
| 1 | 讀取 `.env` 檔 |
| 2 | 把 `.env` 裡的 `DATABASE_URL` 抓出來存進變數 |
| 3 | 用連線字串建立與資料庫的連線 |
| 4 | 建立 cursor，之後用 cursor 執行 SQL |
| 5 | 執行 `SELECT version();` 並把結果存起來 |
| 6 | 印出資料庫版本（看到這個代表成功！） |
| 7 | 關閉 cursor 與連線，釋放資源 |
| 8 | 有任何錯誤都會被這裡接住並印出來 |

在終端機執行：

```bash
python connect_db.py
```

如果看到像這樣的輸出，代表你成功了！

```
✅ 連線成功！PostgreSQL 版本： PostgreSQL 16.x on x86_64-pc-linux-gnu, ...
```

> **進階小提醒（想學更嚴謹的寫法再看）**
>
> 上面的範例在 `try` 區塊內手動關閉連線，好處是好懂。更穩健的寫法是用 `finally`，確保無論成功或失敗，連線都一定會被關閉：
>
> ```python
> try:
>     conn = psycopg2.connect(DATABASE_URL)
>     cur = conn.cursor()
>     cur.execute("SELECT version();")
>     print(cur.fetchone()[0])
> except Exception as e:
>     print("❌ 連線失敗：", e)
> finally:
>     if "conn" in locals() and conn:
>         cur.close()
>         conn.close()
> ```

### 4.2 方法二：拆開的多個變數

如果你的 `.env` 是拆開寫的（PGHOST / PGPORT / PGUSER / PGPASSWORD / PGDATABASE），請用這個寫法：

```python
import os
import psycopg2
from dotenv import load_dotenv

# 1. 讀取 .env 檔案
load_dotenv()

try:
    # 2. 從環境變數一個一個取出連線參數
    conn = psycopg2.connect(
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        dbname=os.getenv("PGDATABASE"),
        sslmode="require",  # Render 的免費 Postgres 需要 SSL
    )

    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print("✅ 連線成功！PostgreSQL 版本：", version[0])

    cur.close()
    conn.close()

except Exception as e:
    print("❌ 連線失敗：", e)
```

> 方法二多了一行 `sslmode="require"`。Render 的免費 PostgreSQL 強制要求 SSL（安全連線），如果你是用「拆開參數」的方式連線，記得加上這一行。

### 4.3 練習：建立資料表並寫入一筆資料

建立 `insert_db.py`，練習「新增」資料：

```python
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # 1. 建立資料表 students（如果還沒有的話）
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            score INT NOT NULL
        );
    """)

    # 2. 插入一筆資料
    cur.execute(
        "INSERT INTO students (name, score) VALUES (%s, %s);",
        ("小明", 95)
    )

    # 3. 很重要！要 commit() 資料才會真的存進去
    conn.commit()
    print("✅ 資料已寫入！")

    # 4. 把資料查回來看看
    cur.execute("SELECT * FROM students;")
    rows = cur.fetchall()
    for row in rows:
        print("學生資料：", row)

    cur.close()
    conn.close()

except Exception as e:
    print("❌ 執行失敗：", e)
```

**幾個重點**：

- `%s` 是 psycopg2 的「佔位符」。不要把資料直接拼進 SQL 字串，這樣可以避免「SQL 注入」攻擊。
- `conn.commit()` 一定要呼叫，否則資料不會真的存進資料庫！
- 寫入後再用 `SELECT` 查回來，是確認資料真的存在的好習慣。

執行：

```bash
python insert_db.py
```

預期輸出：

```
✅ 資料已寫入！
學生資料： (1, '小明', 95)
```

---

## Step 5：實作練習（換你試試看！）

接下來請自己動手做！完成以下任務，並確認每個程式都能成功執行：

1. **任務一**：建立資料表 `fruits`，欄位有 `id`（自動編號）、`name`（水果名）、`price`（價格）。
2. **任務二**：插入至少 3 筆水果資料（例如：蘋果 30、香蕉 15、西瓜 120）。
3. **任務三**：用 `SELECT` 查詢「價格大於 50」的水果。
4. **任務四**：用 `UPDATE` 把其中一筆資料的價格更新，再查詢確認。
5. **任務五**：把你寫的程式碼拿給朋友看，確認**程式碼裡看不到任何密碼**。

> 提示：`UPDATE fruits SET price = %s WHERE name = %s;`

---

## 常見問題（FAQ）與除錯

### Q1：出現 `ModuleNotFoundError: No module named 'psycopg2'`

**原因**：套件沒有安裝，或虛擬環境沒有啟用。

**解法**：

```bash
.venv\Scripts\activate
uv add psycopg2-binary python-dotenv
```

### Q2：出現 `connection failed` 或 `OperationalError`

可能的原因與檢查方向：

| 原因 | 檢查方向 |
|------|----------|
| 連線字串寫錯 | 重新確認 Render 上的 **External Database URL** |
| 用成 Internal 網址 | 本機連線請改用 **External** Database URL |
| 主機位置拼錯 | 確認 `host` 與 Render 顯示的完全一致 |
| 免費額度被停用 | 到 Render 檢查資料庫狀態與剩餘額度 |

### Q3：出現 `password authentication failed for user "xxx"`

**原因**：密碼或使用者名稱錯誤。

**解法**：

1. 確認 `.env` 裡的 `PGPASSWORD` 是 Render 顯示的真實密碼。
2. 確認沒有多打空白或引號。
3. 在 Render 上重設密碼，再更新 `.env`。

### Q4：出現 SSL 相關錯誤

**原因**：Render 免費版要求 SSL 加密連線。

**解法**：連線時加上 `sslmode="require"`：

```python
conn = psycopg2.connect(DATABASE_URL, sslmode="require")
```

### Q5：資料好像沒有存進去？

**原因**：忘了呼叫 `conn.commit()`。

**解法**：執行 `INSERT` / `UPDATE` / `DELETE` 後，一定要呼叫：

```python
conn.commit()
```

### Q6：`.env` 讀不到，`os.getenv()` 回傳 `None`

**原因**：`.env` 檔案位置放錯，或忘了呼叫 `load_dotenv()`。

**解法**：

1. 確認 `.env` 和你的 `.py` 檔案放在同一個資料夾。
2. 確認程式中有呼叫 `load_dotenv()`。
3. 如果 `.env` 在其他資料夾，可以指定路徑：`load_dotenv("其他資料夾/.env")`。

---

## 安全提醒總結

- ✅ 密碼只放在 `.env`，**程式碼中看不到密碼**。
- ✅ 上傳 GitHub 前，確認 `.gitignore` 有忽略 `.env`。
- ✅ 分享專案時，只給 `.env.example` 範本。
- ✅ 隨時檢查你交出去的任何檔案，裡面**不能有密碼**。
- ✅ 密碼外洩時，立刻到 Render 重設密碼。

只要遵守這幾點，你的資料庫就很安全！

---

## 附錄：專案資料夾結構

完成所有步驟後，你的 `backend/08_13/` 資料夾應該長這樣：

```
backend/08_13/
├── .env                  # 🔒 你的密碼（絕不上傳）
├── .env.example          # 範本（可上傳）
├── .gitignore            # 忽略 .env
├── connect_db.py         # 連線測試程式
├── insert_db.py          # 寫入資料範例
└── pyproject.toml        # uv 產生的專案設定
```

---

*恭喜你完成這份教學！動手試試上面的練習題，遇到問題記得回來翻「常見問題」。祝你和你的第一個雲端資料庫相處愉快！*
