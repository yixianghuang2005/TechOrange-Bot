"""A 格：今日科技早報"""
from scraper.rss import get_latest_articles
from utils.gemini_client import summarize_articles


def get_daily_brief() -> str:
    articles = get_latest_articles(limit=5)
    if not articles:
        return "⚠️ 目前無法取得最新文章，請稍後再試。"

    summary = summarize_articles(articles)

    # 附上原文連結
    links = "\n".join([f"🔗 {a['title'][:20]}…\n{a['link']}" for a in articles[:3]])
    return f"🚀 今日科技早報\n\n{summary}\n\n─────────\n{links}"
