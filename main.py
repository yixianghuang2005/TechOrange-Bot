from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi
from linebot.v3.webhooks import MessageEvent, PostbackEvent, TextMessageContent
from linebot.v3.exceptions import InvalidSignatureError
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

configuration = Configuration(access_token=os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))


@app.get("/")
def root():
    return {"status": "TechOrange Bot is running 🚀"}


# ── LINE Webhook ────────────────────────────────────────────
@app.post("/callback")
async def callback(request: Request):
    signature = request.headers.get("X-Line-Signature", "")
    body = await request.body()
    try:
        handler.handle(body.decode("utf-8"), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    return "OK"


# ── Dialogflow Webhook（Fallback → Gemini）──────────────────
@app.post("/webhook")
async def dialogflow_webhook(request: Request):
    """
    Dialogflow 呼叫此端點（Fulfillment）
    在 Default Fallback Intent 開啟 webhook 後，
    使用者問不懂的問題會來這裡，交給 Gemini 回答
    """
    req = await request.json()

    action = req.get("queryResult", {}).get("action", "")
    user_text = req.get("queryResult", {}).get("queryText", "")

    if action == "input.unknown" or not action:
        from utils.gemini_client import ask_gemini
        instruction = (
            "你是 TechOrange 科技智囊助理，專門回答科技、AI、資安相關問題。"
            "請用繁體中文回覆重點，不超過 200 字，不要重述問題。"
        )
        info = ask_gemini(user_text, system_instruction=instruction)
    else:
        info = f"收到動作：{action}"

    return JSONResponse(content={"fulfillmentText": info})


# ── LINE 訊息處理 ───────────────────────────────────────────
@handler.add(MessageEvent, message=TextMessageContent)
def handle_text(event):
    from handlers.message_handler import handle_message
    handle_message(event)


@handler.add(PostbackEvent)
def handle_postback(event):
    from handlers.postback_handler import handle_postback
    handle_postback(event)
