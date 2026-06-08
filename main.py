from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


@app.get("/")
def root():
    return {"status": "TechOrange Bot is running 🚀"}


# ── Dialogflow Fulfillment Webhook ──────────────────────────
# Dialogflow 偵測到 intent 後，呼叫此端點
# 我們根據 intent 名稱呼叫對應功能，回傳 fulfillmentText 給 LINE
@app.post("/webhook")
async def dialogflow_webhook(request: Request):
    req = await request.json()

    intent_name = req.get("queryResult", {}).get("intent", {}).get("displayName", "")
    user_text   = req.get("queryResult", {}).get("queryText", "")

    info = dispatch_intent(intent_name, user_text)

    return JSONResponse(content={"fulfillmentText": info})


def dispatch_intent(intent_name: str, user_text: str) -> str:
    """根據 intent 名稱呼叫對應功能"""

    if intent_name == "daily_brief":
        from features.news.daily_brief import get_daily_brief
        return get_daily_brief()

    elif intent_name == "ai_consultant":
        # 請使用者輸入行業別
        return "🧠 AI 落地顧問\n\n請輸入您的行業別，我會幫您生成 AI 轉型建議！\n\n例如：「我是零售業」、「製造業」、「餐飲業」"

    elif intent_name == "security":
        from features.security.alert import get_security_alert
        return get_security_alert()

    elif intent_name == "keyword":
        return (
            "🔍 關鍵字科普\n\n"
            "請輸入想了解的科技詞彙，例如：\n"
            "• 什麼是 RAG？\n"
            "• 解釋 Agentic AI\n"
            "• MCP 是什麼\n"
            "• 邊緣運算"
        )

    elif intent_name == "industry":
        from features.industry.transform import get_transform_cases
        return get_transform_cases()

    elif intent_name == "settings":
        from features.subscription.settings import show_settings
        return show_settings("")

    else:
        # Default Fallback Intent → Gemini 回答
        from utils.gemini_client import ask_gemini
        instruction = (
            "你是 TechOrange 科技智囊助理，專門回答科技、AI、資安相關問題。"
            "請用繁體中文回覆重點，不超過 200 字，不要重述問題。"
        )
        return ask_gemini(user_text, system_instruction=instruction)
