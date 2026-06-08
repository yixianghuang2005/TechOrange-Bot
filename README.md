# 🍊 TechOrange 科技新聞機器人

> 靜宜大學 資訊管理導論 期末專案

一個整合 TechOrange（科技報橘）的 LINE 聊天機器人，讓使用者透過 LINE 快速掌握最新科技趨勢、AI 動態與資安預警，無需開啟網站即可獲取資訊。

---

## 📱 功能介紹（六宮格）

| 格 | 功能 | 說明 |
|----|------|------|
| 🚀 | **今日科技早報** | 抓取 TechOrange 最新 5 篇文章 |
| 🧠 | **AI 相關** | 過濾 AI 類別文章即時呈現 |
| 🛡️ | **資安相關** | 最新資安威脅新聞 |
| 🔍 | **關鍵字科普** | 輸入詞彙，Gemini AI 白話解釋 |
| 🏭 | **產業轉型** | 數位轉型、智慧製造相關報導 |
| ⚙️ | **使用說明** | Bot 功能介紹 |

---

## 🛠️ 技術堆疊

| 層級 | 工具 |
|------|------|
| 語言 | Python 3.11 |
| Web 框架 | FastAPI |
| 資料抓取 | requests + BeautifulSoup（RSS XML 解析）|
| 意圖辨識 | Dialogflow ES |
| AI 回覆 | Gemini API（gemini-2.0-flash-lite）|
| 資料庫 | Firebase Firestore |
| 部署 | Vercel |
| LINE 整合 | LINE Messaging API + Dialogflow LINE Integration |

---

## 🏗️ 系統架構

```
使用者 → LINE Bot
            │
            ▼
    Dialogflow ES（意圖辨識）
            │
            ▼
    Vercel /webhook（FastAPI）
            │
    ┌───────┴────────┐
    │                │
    ▼                ▼
TechOrange      Gemini API
RSS 爬蟲        （關鍵字科普
（requests +     & Fallback）
 BeautifulSoup）
```

---

## 📁 專案結構

```
TechOrange-Bot/
├── main.py                   # FastAPI 主程式 + Dialogflow webhook
├── requirements.txt
├── vercel.json
├── api/
│   └── index.py              # Vercel 入口
├── features/
│   ├── news/daily_brief.py   # 今日科技早報
│   ├── ai/consultant.py      # AI 相關新聞
│   ├── security/alert.py     # 資安預警
│   ├── explainer/keyword.py  # 關鍵字科普
│   ├── industry/transform.py # 產業轉型
│   └── subscription/settings.py # 使用說明
├── scraper/
│   └── rss.py                # RSS 爬蟲工具
├── utils/
│   └── gemini_client.py      # Gemini API 封裝
├── db/
│   └── firebase.py           # Firebase 快取
├── dialogflow/
│   └── client.py             # Dialogflow 封裝
└── rich_menu/
    └── setup_menu.py         # LINE Rich Menu 設定
```

---

## ⚙️ 環境變數

複製 `.env.example` 為 `.env` 並填入：

```env
LINE_CHANNEL_SECRET=
LINE_CHANNEL_ACCESS_TOKEN=
DIALOGFLOW_PROJECT_ID=
GOOGLE_APPLICATION_CREDENTIALS=
FIREBASE_CREDENTIALS=
GEMINI_API_KEY=
```

---

## 🚀 本機執行

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 📊 資料來源

- 新聞：[techorange.com](https://techorange.com)（RSS Feed）
- AI 回覆：Google Gemini API
- 意圖辨識：Google Dialogflow ES

---

## 👥 開發團隊

靜宜大學 資訊管理系 | 資訊管理導論 期末專案
組長:黃義祥
組員:王奕翔、黃士豪、張佑先
