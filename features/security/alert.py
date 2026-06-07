"""C 格：資安預警"""
from scraper.rss import get_security_articles
from utils.gemini_client import ask_gemini


def get_security_alert() -> str:
    articles = get_security_articles(limit=5)
    if not articles:
        return "⚠️ 目前無法取得資安資訊，請稍後再試。"

    context = "\n\n".join([
        f"【{a['title']}】\n{a['excerpt']}\n來源：{a['link']}"
        for a in articles
    ])

    prompt = f"""請根據以下資安新聞，整理成企業實用的資安預警報告。

格式：
🛡️ 本週重大資安事件（2~3 條，各一句說明）
✅ 企業自我檢查清單（3 項，具體可執行）

全部繁體中文，不超過 300 字。

資安新聞：
{context}
"""
    result = ask_gemini(prompt)
    return f"🛡️ 資安預警\n\n{result}"
