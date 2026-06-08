from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


@app.get("/")
def root():
    return {"status": "TechOrange Bot is running 🚀"}


@app.post("/webhook")
async def dialogflow_webhook(request: Request):
    try:
        req = await request.json()
        intent_name = req.get("queryResult", {}).get("intent", {}).get("displayName", "")
        user_text   = req.get("queryResult", {}).get("queryText", "")
        info = dispatch_intent(intent_name, user_text)
        return JSONResponse(content={"fulfillmentText": info})
    except Exception as e:
        return JSONResponse(content={"fulfillmentText": f"系統錯誤：{str(e)}"})


def dispatch_intent(intent_name: str, user_text: str) -> str:
    try:
        if intent_name == "daily_brief":
            return _get_daily_brief()          # ← 直接 RSS，不用 AI

        elif intent_name == "ai_consultant":
            return _get_ai_news()   # ← 直接顯示 AI 類新聞

        elif intent_name == "security":
            return _get_security()             # ← 直接 RSS，不用 AI

        elif intent_name == "keyword":
            # 清理關鍵字
            keyword = user_text
            for w in ["什麼是", "解釋一下", "解釋", "關鍵字科普", "關鍵字", "？", "?"]:
                keyword = keyword.replace(w, "")
            keyword = keyword.strip()

            if not keyword:
                # 使用者只按了按鈕，還沒輸入詞彙
                return (
                    "🔍 關鍵字科普\n\n"
                    "請輸入想了解的科技詞彙！\n\n"
                    "例如：\n"
                    "• 什麼是 RAG？\n"
                    "• 解釋 Agentic AI\n"
                    "• MCP 是什麼\n"
                    "• 邊緣運算"
                )
            return _explain_keyword(keyword)   # ← 有詞彙才呼叫 Gemini

        elif intent_name == "industry":
            return _get_industry()             # ← 直接 RSS，不用 AI

        elif intent_name == "settings":
            from features.subscription.settings import show_settings
            return show_settings("")

        else:
            # 使用者問了無關的問題 → Gemini 回答
            return _ask_gemini(user_text)

    except Exception as e:
        return f"⚠️ 發生錯誤：{str(e)}"


# ── 新聞類：直接顯示 RSS 標題 + 連結，不呼叫 AI ─────────────

def _get_daily_brief() -> str:
    import requests
    from bs4 import BeautifulSoup

    res = requests.get("https://techorange.com/feed/", timeout=10)
    soup = BeautifulSoup(res.content, "xml")
    items = soup.find_all("item")[:5]

    lines = []
    for item in items:
        title = item.find("title").text.strip()
        link  = item.find("link").text.strip()
        lines.append(f"📌 {title}\n🔗 {link}")

    return "🚀 今日科技早報\n\n" + "\n\n".join(lines)


def _get_ai_news() -> str:
    import requests
    from bs4 import BeautifulSoup

    res = requests.get("https://techorange.com/feed/", timeout=10)
    soup = BeautifulSoup(res.content, "xml")
    items = soup.find_all("item")

    # 過濾 AI 類文章
    ai_items = []
    for item in items:
        cats = [c.text for c in item.find_all("category")]
        if any("AI" in c for c in cats):
            ai_items.append(item)

    if not ai_items:
        ai_items = items[:5]

    lines = []
    for item in ai_items[:5]:
        title = item.find("title").text.strip()
        link  = item.find("link").text.strip()
        lines.append(f"🧠 {title}\n🔗 {link}")

    return "🧠 AI 相關新聞\n\n" + "\n\n".join(lines)


def _get_security() -> str:
    import requests
    from bs4 import BeautifulSoup

    res = requests.get(
        "https://techorange.com/category/cybersecurity/feed/", timeout=10
    )
    soup = BeautifulSoup(res.content, "xml")
    items = soup.find_all("item")[:5]

    lines = []
    for item in items:
        title = item.find("title").text.strip()
        link  = item.find("link").text.strip()
        lines.append(f"🛡️ {title}\n🔗 {link}")

    return "🛡️ 最新資安預警\n\n" + "\n\n".join(lines)


def _get_industry() -> str:
    import requests
    from bs4 import BeautifulSoup

    res = requests.get("https://techorange.com/feed/", timeout=10)
    soup = BeautifulSoup(res.content, "xml")
    items = soup.find_all("item")[:15]

    keywords = ["數位轉型", "智慧製造", "ESG", "供應鏈", "中小企業", "自動化", "工廠"]
    lines = []
    for item in items:
        title = item.find("title").text.strip()
        link  = item.find("link").text.strip()
        if any(kw in title for kw in keywords):
            lines.append(f"🏭 {title}\n🔗 {link}")

    if not lines:
        for item in items[:3]:
            title = item.find("title").text.strip()
            link  = item.find("link").text.strip()
            lines.append(f"🏭 {title}\n🔗 {link}")

    return "🏭 產業轉型案例\n\n" + "\n\n".join(lines)


# ── AI 類：只有關鍵字科普和 Fallback 呼叫 Gemini ────────────

def _explain_keyword(keyword: str) -> str:
    if not keyword:
        return "🔍 請輸入想了解的科技詞彙，例如：「什麼是 RAG？」"
    prompt = (
        f"請用「高中生都能懂的方式」解釋「{keyword}」。\n"
        "格式：①一句話定義 ②生活化比喻 ③台灣應用案例 ④為什麼重要\n"
        "繁體中文，不超過 200 字。"
    )
    return f"🔍 {keyword} 是什麼？\n\n" + _ask_gemini(prompt)


def _ask_gemini(prompt: str) -> str:
    try:
        from google import genai
        from google.genai import types

        api_key = os.getenv("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)

        config = types.GenerateContentConfig(
            max_output_tokens=400,
            system_instruction="你是 TechOrange 科技智囊助理，請用繁體中文簡潔回答。"
        )
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=config,
        )
        return response.text if response.text else "抱歉，AI 暫時無法回應。"
    except Exception as e:
        return f"⚠️ AI 錯誤：{str(e)[:150]}"
