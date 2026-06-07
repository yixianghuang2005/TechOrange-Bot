# TechOrange 科技智囊 LINE Bot
資訊管理導論期末專案 — TechOrange 科技智囊聊天機器人

幫你快速掌握最新科技趨勢、AI 動態、資安預警。

## 架構
```
程式碼 → GitHub → Vercel → Firebase + Dialogflow + LINE Bot
```

## 六宮格功能
| 格 | 功能 |
|----|------|
| A 🚀 | 今日科技早報 |
| B 🧠 | AI 落地顧問 |
| C 🛡️ | 資安預警 |
| D 🔍 | 關鍵字科普 |
| E 🏭 | 產業轉型案例 |
| F ⚙️ | 訂閱設定 |

## 建置步驟
1. `cp .env.example .env` 並填入所有金鑰
2. `pip install -r requirements.txt`
3. 先測試爬蟲：`python tests/test_scraper.py`
4. 本地啟動：`uvicorn main:app --reload`
5. ngrok 開 tunnel：`ngrok http 8000`
6. LINE Developer Console 設 webhook URL

## 開發工具
Python / FastAPI / LINE Bot SDK v3 / Dialogflow ES / Firebase / Vercel / Gemini API
