from fastapi import FastAPI, Request, HTTPException
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi
from linebot.v3.webhooks import MessageEvent, PostbackEvent, TextMessageContent
from linebot.v3.exceptions import InvalidSignatureError
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# LINE Bot 設定
configuration = Configuration(access_token=os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))


@app.get("/")
def root():
    return {"status": "TechOrange Bot is running 🚀"}


@app.post("/callback")
async def callback(request: Request):
    """LINE Webhook 入口"""
    signature = request.headers.get("X-Line-Signature", "")
    body = await request.body()
    try:
        handler.handle(body.decode("utf-8"), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    return "OK"


# ── 文字訊息：交給 Dialogflow 判斷意圖 ──────────────────────
@handler.add(MessageEvent, message=TextMessageContent)
def handle_text(event):
    from handlers.message_handler import handle_message
    handle_message(event)


# ── 按鈕點擊（Rich Menu postback）：直接 dispatch ──────────
@handler.add(PostbackEvent)
def handle_postback(event):
    from handlers.postback_handler import handle_postback
    handle_postback(event)
