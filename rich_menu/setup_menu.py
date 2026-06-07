"""
一次性腳本：建立 LINE 六宮格 Rich Menu
執行方式：python rich_menu/setup_menu.py

執行前請確認：
  1. .env 裡的 LINE_CHANNEL_ACCESS_TOKEN 已填好
  2. 準備好 rich_menu/menu.png（1200x810 的選單圖片）
"""
import os, requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# ── 六宮格設定 ──────────────────────────────────────────────
rich_menu_body = {
    "size": {"width": 2500, "height": 1686},
    "selected": True,
    "name": "TechOrange 科技智囊",
    "chatBarText": "📱 開啟選單",
    "areas": [
        # A. 今日科技早報（左上）
        {"bounds": {"x": 0,    "y": 0,    "width": 1250, "height": 843},
         "action": {"type": "postback", "data": "action=daily_brief",  "displayText": "🚀 今日科技早報"}},
        # B. AI 落地顧問（右上）
        {"bounds": {"x": 1250, "y": 0,    "width": 1250, "height": 843},
         "action": {"type": "postback", "data": "action=ai_consultant","displayText": "🧠 AI 落地顧問"}},
        # C. 資安預警（左中）
        {"bounds": {"x": 0,    "y": 843,  "width": 1250, "height": 843},
         "action": {"type": "postback", "data": "action=security",     "displayText": "🛡️ 資安預警"}},
        # D. 關鍵字科普（右中）
        {"bounds": {"x": 1250, "y": 843,  "width": 1250, "height": 843},
         "action": {"type": "postback", "data": "action=keyword",      "displayText": "🔍 關鍵字科普"}},
        # E. 產業轉型（左下）
        {"bounds": {"x": 0,    "y": 1686, "width": 1250, "height": 843},
         "action": {"type": "postback", "data": "action=industry",     "displayText": "🏭 產業轉型案例"}},
        # F. 訂閱設定（右下）
        {"bounds": {"x": 1250, "y": 1686, "width": 1250, "height": 843},
         "action": {"type": "postback", "data": "action=settings",     "displayText": "⚙️ 訂閱設定"}},
    ]
}

# 1. 建立 Rich Menu
res = requests.post(
    "https://api.line.me/v2/bot/richmenu",
    headers=HEADERS, json=rich_menu_body
)
rich_menu_id = res.json().get("richMenuId")
print("Rich Menu 建立成功，ID:", rich_menu_id)

# 2. 上傳圖片（需要準備 rich_menu/menu.png）
menu_image_path = os.path.join(os.path.dirname(__file__), "menu.png")
if os.path.exists(menu_image_path):
    with open(menu_image_path, "rb") as f:
        img_res = requests.post(
            f"https://api-data.line.me/v2/bot/richmenu/{rich_menu_id}/content",
            headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "image/png"},
            data=f
        )
    print("圖片上傳:", img_res.status_code)
else:
    print("⚠️ 找不到 rich_menu/menu.png，請先設計圖片再上傳")

# 3. 設為預設選單
default_res = requests.post(
    f"https://api.line.me/v2/bot/user/all/richmenu/{rich_menu_id}",
    headers=HEADERS
)
print("設為預設:", default_res.status_code)
print("✅ 完成！重新開啟 LINE Bot 就能看到選單")
