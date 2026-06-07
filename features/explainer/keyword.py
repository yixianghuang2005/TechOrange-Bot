"""D 格：關鍵字科普"""
from scraper.rss import get_articles_by_keyword
from utils.gemini_client import explain_keyword as gemini_explain

# 熱門關鍵字清單（點 D 格時顯示）
HOT_KEYWORDS = [
    "RAG", "Agentic AI", "MCP", "邊緣運算",
    "主權 AI", "量子運算", "數位分身", "RLHF"
]


def explain_keyword(keyword: str) -> str:
    # 搜尋相關文章作為參考
    articles = get_articles_by_keyword(keyword, limit=3)
    result = gemini_explain(keyword, articles)
    return f"🔍 {keyword} 是什麼？\n\n{result}"


def get_keyword_menu() -> str:
    """顯示熱門關鍵字選單"""
    kw_list = "\n".join([f"• {kw}" for kw in HOT_KEYWORDS])
    return f"🔍 關鍵字科普\n\n請輸入想了解的科技詞彙，或從以下熱門關鍵字選擇：\n\n{kw_list}"
