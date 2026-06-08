"""
Dialogflow ES 封裝
用途：送出使用者文字，取得意圖（intent）名稱與參數
"""
import os
import json
import tempfile
from google.cloud import dialogflow_v2 as dialogflow
from google.oauth2 import service_account


def _get_credentials():
    """支援環境變數 JSON 字串（Vercel）或檔案路徑（本機）"""
    cred_env = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
    if cred_env.strip().startswith("{"):
        # Vercel：環境變數直接是 JSON 內容
        cred_dict = json.loads(cred_env)
        return service_account.Credentials.from_service_account_info(
            cred_dict,
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
    return None  # 本機：使用 ADC 或檔案路徑


def detect_intent(session_id: str, text: str, language: str = "zh-TW") -> tuple:
    """
    送文字給 Dialogflow，回傳 (intent名稱, 參數字典)
    session_id 用 LINE user_id，讓每個用戶有獨立對話
    """
    project_id = os.getenv("DIALOGFLOW_PROJECT_ID", "techorange-bot")
    credentials = _get_credentials()

    if credentials:
        session_client = dialogflow.SessionsClient(credentials=credentials)
    else:
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
