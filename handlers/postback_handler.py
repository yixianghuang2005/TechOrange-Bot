"""
Rich Menu 按鈕點擊處理
按鈕傳來 postback data → 直接呼叫功能（不過 Dialogflow）

Rich Menu 按鈕設定的 data 值：
  A → action=daily_brief
  B → action=ai_consultant
  C → action=security
  D → action=keyword
  E → action=industry
  F → action=settings
"""
import os
from linebot.v3.messaging import (
    ApiClient, Configuration, MessagingApi, ReplyMessageRequest, TextMessage
)

configuration = Configuration(access_token=os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))


def handle_postback(event):
    data = event.postback.data
    user_id = event.source.user_id
    reply_token = event.reply_token

    params = dict(p.split("=") for p in data.split("&") if "=" in p)
    action = params.get("action", "")

    reply = dispatch_action(action, user_id)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(ReplyMessageRequest(
            reply_token=reply_token,
            messages=[TextMessage(text=reply)]
        ))


def dispatch_action(action: str, user_id: str) -> str:
    if action == "daily_brief":
        from features.news.daily_brief import get_daily_brief
        return get_daily_brief()

    elif action == "ai_consultant":
        return "🧠 AI 落地顧問\n\n請輸入您的行業別，我會幫您生成 AI 轉型建議！\n\n例如：「我是零售業」、「我是製造業」"

    elif action == "security":
        from features.security.alert import get_security_alert
        return get_security_alert()

    elif action == "keyword":
        return (
            "🔍 關鍵字科普\n\n"
            "請輸入想了解的科技詞彙，例如：\n"
            "• 什麼是 RAG？\n"
            "• 解釋 Agentic AI\n"
            "• MCP 是什麼\n"
            "• 邊緣運算"
        )

    elif action == "industry":
        from features.industry.transform import get_transform_cases
        return get_transform_cases()

    elif action == "settings":
        from features.subscription.settings import show_settings
        return show_settings(user_id)

    else:
        return "請點選下方選單選擇功能 🙂"
