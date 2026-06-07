"""E 格：產業轉型案例"""
from scraper.rss import get_latest_articles
from utils.gemini_client import ask_gemini

TRANSFORM_KEYWORDS = ["數位轉型", "智慧製造", "ESG", "供應鏈", "中小企業", "自動化", "工廠"]


def get_transform_cases() -> str:
    articles = get_latest_articles(limit=50)

    # 過濾含轉型關鍵字的文章
    filtered = [
        a for a in articles
        if any(kw in a["title"] + a["excerpt"] for kw in TRANSFORM_KEYWORDS)
    ]

    if not filtered:
        filtered = articles[:5]  # 沒有就用最新的

    context = "\n\n".join([
        f"【{a['title']}】\n{a['excerpt']}\n來源：{a['link']}"
        for a in filtered[:5]
    ])

    prompt = f"""請從以下文章中，找出最適合台灣中小企業參考的產業轉型案例。

格式：
🏭 精選轉型案例（3 個）
每個案例：企業名 / 做了什麼 / 成效 / 參考連結

原則：選「台灣企業看得到、吃得到、複製得了」的案例。
全部繁體中文，不超過 350 字。

文章：
{context}
"""
    result = ask_gemini(prompt, max_tokens=600)
    return f"🏭 產業轉型案例\n\n{result}"
