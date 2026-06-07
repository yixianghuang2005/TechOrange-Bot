"""
TechOrange RSS 爬蟲
工具：requests + BeautifulSoup（和上課一模一樣，只是 parser 換成 'xml'）

可用的 RSS：
  主 Feed:  https://techorange.com/feed/            （所有分類，約 16~20 篇）
  資安專區: https://techorange.com/category/cybersecurity/feed/
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from db.firebase import cache_get, cache_set


RSS_MAIN     = "https://techorange.com/feed/"
RSS_SECURITY = "https://techorange.com/category/cybersecurity/feed/"


def _clean_url(url: str) -> str:
    """去掉 UTM 追蹤參數，保留乾淨網址"""
    p = urlparse(url.strip())
    return f"{p.scheme}://{p.netloc}{p.path}"


def _parse_rss(url: str) -> list[dict]:
    """用 requests + BeautifulSoup 抓 RSS，回傳文章列表"""
    headers = {"User-Agent": "Mozilla/5.0 (TechOrange Bot)"}
    res = requests.get(url, headers=headers, timeout=10)
    res.raise_for_status()

    # ← 這裡和上課唯一的差別：parser 用 'xml' 而不是 'html.parser'
    soup = BeautifulSoup(res.content, "xml")

    articles = []
    for item in soup.find_all("item"):
        # 標題
        title = item.find("title").text.strip()

        # 連結
        link = _clean_url(item.find("link").text)

        # 日期
        pub_date = item.find("pubDate").text.strip() if item.find("pubDate") else ""

        # 分類標籤（可多個，例如 ["AI 人工智慧", "資安"]）
        categories = [c.text.strip() for c in item.find_all("category")]

        # 摘要（description 是 HTML，用 BS4 再解析一次去掉標籤）
        desc_raw = item.find("description").text if item.find("description") else ""
        excerpt  = BeautifulSoup(desc_raw, "html.parser").get_text()[:200].strip()

        # 完整全文（content:encoded，約 3500 字，給 Gemini RAG 用）
        encoded   = item.find("encoded")
        full_text = BeautifulSoup(encoded.text, "html.parser").get_text() if encoded else excerpt

        articles.append({
            "title":      title,
            "link":       link,
            "date":       pub_date,
            "categories": categories,
            "excerpt":    excerpt,
            "full_text":  full_text,
        })

    return articles


# ── 公開函式（供各 feature 呼叫）────────────────────────────


def get_latest_articles(limit: int = 5) -> list[dict]:
    """取最新文章，結果快取 30 分鐘"""
    cache_key = f"rss_main_{limit}"
    cached = cache_get(cache_key)
    if cached:
        return cached[:limit]

    articles = _parse_rss(RSS_MAIN)
    cache_set(cache_key, articles, ttl_minutes=30)
    return articles[:limit]


def get_articles_by_category(category: str, limit: int = 10) -> list[dict]:
    """從主 Feed 過濾指定分類的文章"""
    all_articles = get_latest_articles(limit=50)
    filtered = [a for a in all_articles if category in a["categories"]]
    return filtered[:limit]


def get_articles_by_keyword(keyword: str, limit: int = 5) -> list[dict]:
    """從主 Feed 搜尋標題或全文含關鍵字的文章"""
    all_articles = get_latest_articles(limit=50)
    keyword_lower = keyword.lower()
    filtered = [
        a for a in all_articles
        if keyword_lower in a["title"].lower() or keyword_lower in a["full_text"].lower()
    ]
    return filtered[:limit]


def get_security_articles(limit: int = 5) -> list[dict]:
    """專門抓資安分類的文章"""
    cache_key = f"rss_security_{limit}"
    cached = cache_get(cache_key)
    if cached:
        return cached[:limit]

    articles = _parse_rss(RSS_SECURITY)
    cache_set(cache_key, articles, ttl_minutes=30)
    return articles[:limit]
