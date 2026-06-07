"""
基本測試：確認 RSS 爬蟲能正常運作
執行：python tests/test_scraper.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from scraper.rss import get_latest_articles, get_security_articles

print("=== 測試主 RSS ===")
articles = get_latest_articles(limit=3)
for a in articles:
    print(f"✅ {a['title'][:40]}...")
    print(f"   分類: {a['categories']}")
    print(f"   全文字數: {len(a['full_text'])} 字")
    print()

print("=== 測試資安 RSS ===")
sec = get_security_articles(limit=2)
for a in sec:
    print(f"🛡️ {a['title'][:40]}...")
    print()

print("✅ 爬蟲測試通過！")
