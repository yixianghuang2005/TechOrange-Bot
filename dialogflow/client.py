"""
Dialogflow ES 封裝
用途：送出使用者文字，取得意圖（intent）名稱與參數
"""
import os
from google.cloud import dialogflow_v2 as dialogflow


def detect_intent(session_id: str, text: str, language: str = "zh-TW") -> tuple[str, dict]:
    """
    送文字給 Dialogflow，回傳 (intent名稱, 參數字典)
    session_id 用 LINE user_id 就好，讓每個用戶有獨立對話
    """
    project_id = os.getenv("DIALOGFLOW_PROJECT_ID")

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    intent_name = response.query_result.intent.display_name
    parameters  = dict(response.query_result.parameters)

    return intent_name, parameters
