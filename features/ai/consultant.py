"""B 格：AI 落地顧問（RAG）"""
from scraper.rss import get_articles_by_category, get_latest_articles
from utils.gemini_client import rag_industry_advice


def get_ai_advice(industry: str) -> str:
    # 先抓 AI 類文章
    articles = get_articles_by_category("AI 人工智慧", limit=20)
    if not articles:
        articles = get_latest_articles(limit=10)

    advice = rag_industry_advice(industry, articles)
    return f"🧠 {industry}業 AI 轉型建議\n\n{advice}"
