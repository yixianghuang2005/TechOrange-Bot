"""F 格：訂閱設定"""
from db.firebase import get_user_settings, save_user_settings


def show_settings(user_id: str) -> str:
    settings = get_user_settings(user_id)
    push = "✅ 已開啟" if settings.get("push_enabled") else "❌ 未開啟"
    time = settings.get("push_time", "09:00")
    return (
        f"⚙️ 我的訂閱設定\n\n"
        f"每日推播：{push}\n"
        f"推播時間：{time}\n\n"
        f"輸入以下指令修改：\n"
        f"• 「開啟推播」/ 「關閉推播」\n"
        f"• 「設定時間 HH:MM」（例如：設定時間 08:30）"
    )


def update_push(user_id: str, enabled: bool) -> str:
    save_user_settings(user_id, {"push_enabled": enabled})
    status = "已開啟" if enabled else "已關閉"
    return f"✅ 每日推播{status}！"


def update_push_time(user_id: str, time_str: str) -> str:
    save_user_settings(user_id, {"push_time": time_str})
    return f"✅ 推播時間已設為 {time_str}"
