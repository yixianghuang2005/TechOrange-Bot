"""
Firebase Firestore 封裝
用途：
  1. 快取 RSS 爬蟲結果（避免每次都打 TechOrange）
  2. 存用戶訂閱設定
"""
import os
import json
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials, firestore

_db = None

def _get_db():
    global _db
    if _db is None:
        if not firebase_admin._apps:
            # 支援兩種方式：JSON 字串（Vercel）或檔案路徑（本機）
            cred_env = os.getenv("FIREBASE_CREDENTIALS", "")
            if cred_env.strip().startswith("{"):
                # Vercel：環境變數直接是 JSON 內容
                cred_dict = json.loads(cred_env)
                cred = credentials.Certificate(cred_dict)
            else:
                # 本機：JSON 檔案路徑
                cred_path = cred_env or "firebase-service-account.json"
                cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        _db = firestore.client()
    return _db


def cache_get(key: str):
    try:
        db = _get_db()
        doc = db.collection("cache").document(key).get()
        if not doc.exists:
            return None
        data = doc.to_dict()
        if datetime.utcnow() > data.get("expires_at").replace(tzinfo=None):
            return None
        return data.get("value")
    except Exception as e:
        print(f"[Firebase] cache_get 失敗: {e}")
        return None


def cache_set(key: str, value, ttl_minutes: int = 30):
    try:
        db = _get_db()
        expires_at = datetime.utcnow() + timedelta(minutes=ttl_minutes)
        db.collection("cache").document(key).set({
            "value":      value,
            "expires_at": expires_at,
            "updated_at": datetime.utcnow(),
        })
    except Exception as e:
        print(f"[Firebase] cache_set 失敗: {e}")


def get_user_settings(user_id: str) -> dict:
    try:
        db = _get_db()
        doc = db.collection("users").document(user_id).get()
        if doc.exists:
            return doc.to_dict()
    except Exception as e:
        print(f"[Firebase] get_user_settings 失敗: {e}")
    return {"push_enabled": False, "push_time": "09:00", "interests": []}


def save_user_settings(user_id: str, settings: dict):
    try:
        db = _get_db()
        db.collection("users").document(user_id).set(settings, merge=True)
    except Exception as e:
        print(f"[Firebase] save_user_settings 失敗: {e}")
