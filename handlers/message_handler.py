"""
文字輸入處理：
  使用者輸入文字 → Dialogflow 判斷意圖 → 呼叫對應功能
"""
import os
from linebot.v3.messaging import (
    ApiClient, Configuration, MessagingApi, ReplyMessageRequest, TextMessage
)
from dialogflow.client import detect_intent

configuration = Configuration(access_token=os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))


def handle_message(event):
    user_text = event.message.text
    user_id   = event.source.user_id
    reply_token = event.reply_token

    # Dialogflow 判斷意圖
    intent, parameters = detect_intent(user_id, user_text)

    # 根據意圖呼叫對應功能
    reply = dispatch(intent, parameters, user_id, user_text)

    # 回傳給 LINE
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(ReplyMessageRequest(
            reply_token=reply_token,
            messages=[TextMessage(text=reply)]
        ))


def dispatch(intent: str, parameters: dict, user_id: str, raw_text: str) -> str:
    """根據 Dialogflow intent 呼叫對應功能"""

    if intent == "daily_brief":
        from features.news.daily_brief import get_daily_brief
        return get_daily_brief()

    elif intent == "ai_consultant":
        industry = parameters.get("industry", "")
        if not industry:
            return "請問您是哪個行業？（例如：零售業、製造業、金融業）"
        from features.ai.consultant import get_ai_advice
        return get_ai_advice(industry)

    elif intent == "security":
        from features.security.alert import get_security_alert
        return get_security_alert()

    elif intent == "keyword":
        keyword = parameters.get("keyword", raw_text)
        from features.explainer.keyword import explain_keyword
        return explain_keyword(keyword)

    elif intent == "industry":
        from features.industry.transform import get_transform_cases
        return get_transform_cases()

    elif intent == "settings":
        from features.subscription.settings import show_settings
        return show_settings(user_id)

    else:
        # Fallback：用 Gemini 直接回答
        from utils.gemini_client import ask_gemini
        return ask_gemini(f"請根據科技趨勢回答：{raw_text}")
