"""
Gemini API 封裝
用途：文章摘要、RAG 問答、關鍵字解釋
"""
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
_model = genai.GenerativeModel("gemini-2.0-flash")


def ask_gemini(prompt: str, max_tokens: int = 500) -> str:
    """送 prompt 給 Gemini，回傳文字結果"""
    try:
        response = _model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=0.7,
            )
        )
        return response.text.strip()
    except Exception as e:
        return f"⚠️ AI 暫時無法回應，請稍後再試。（{e}）"


def summarize_articles(articles: list[dict]) -> str:
    """把多篇文章濃縮成 LINE 可讀的早報格式"""
    if not articles:
        return "目前暫無最新文章。"

    article_text = "\n\n".join([
        f"標題：{a['title']}\n摘要：{a['excerpt']}"
        for a in articles
    ])

    prompt = f"""你是科技新聞編輯，請將以下 TechOrange 文章整理成「30 秒科技早報」。

格式要求：
- 每篇用「📌 標題 + 一句精華重點」呈現
- 最後加一行「📎 今日關鍵詞：xxx、xxx、xxx」
- 全部用繁體中文
- 不超過 300 字

文章內容：
{article_text}
"""
    return ask_gemini(prompt)


def rag_industry_advice(industry: str, articles: list[dict]) -> str:
    """RAG：根據文章內容，為指定行業生成 AI 導入建議"""
    if not articles:
        return f"目前沒有找到與 {industry} 相關的文章，請稍後再試。"

    context = "\n\n".join([
        f"【{a['title']}】\n{a['full_text'][:800]}\n來源：{a['link']}"
        for a in articles[:5]
    ])

    prompt = f"""你是企業 AI 顧問，請根據以下 TechOrange 科技報導，
為「{industry}業」的台灣中小企業生成 AI 轉型建議。

要求：
1. 列出 3 個具體可執行的建議
2. 每項建議附上參考文章連結
3. 避免過度理想化，要台灣企業能做到的
4. 用繁體中文，不超過 350 字

參考文章：
{context}
"""
    return ask_gemini(prompt, max_tokens=600)


def explain_keyword(keyword: str, articles: list[dict]) -> str:
    """用白話文解釋科技關鍵字，搭配台灣案例"""
    context = ""
    if articles:
        context = "\n\n".join([
            f"【{a['title']}】\n{a['excerpt']}\n來源：{a['link']}"
            for a in articles[:3]
        ])
        context = f"\n\n相關報導：\n{context}"

    prompt = f"""請用「高中生都能懂的方式」解釋「{keyword}」這個科技名詞。

格式：
1. 一句話定義（30 字內）
2. 生活化比喻說明
3. 台灣目前的應用案例（1~2 個）
4. 為什麼現在很重要？
全部繁體中文，不超過 250 字。{context}
"""
    return ask_gemini(prompt)
