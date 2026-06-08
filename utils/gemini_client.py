"""
Gemini API 封裝
上課寫法：from google import genai + client.models.generate_content()
環境變數名稱：GEMINI_API_KEY（Vercel 和本機都用這個名稱）
"""
from google import genai
from google.genai import types

# SDK 自動讀取環境變數 GEMINI_API_KEY，不需要手動傳入
client = genai.Client()

MODEL = "gemini-2.0-flash"   # 或 gemini-2.0-flash-lite（速度更快）


def ask_gemini(prompt: str, system_instruction: str = None) -> str:
    """基本問答（和上課寫法相同）"""
    try:
        if system_instruction:
            ai_config = types.GenerateContentConfig(
                max_output_tokens=500,
                system_instruction=system_instruction
            )
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=ai_config,
            )
        else:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
            )
        return response.text if response.text else "抱歉，我現在無法生成回應，請稍後再試。"
    except Exception as e:
        return f"⚠️ AI 暫時無法回應，請稍後再試。"


def summarize_articles(articles: list[dict]) -> str:
    """把多篇文章濃縮成 30 秒早報"""
    if not articles:
        return "目前暫無最新文章。"

    article_text = "\n\n".join([
        f"標題：{a['title']}\n摘要：{a['excerpt']}"
        for a in articles
    ])

    prompt = f"""請將以下 TechOrange 文章整理成「30 秒科技早報」。
格式：每篇用「📌 標題 + 一句精華重點」呈現，最後加「📎 今日關鍵詞：xxx、xxx」
全部繁體中文，不超過 300 字。

文章內容：
{article_text}
"""
    instruction = "你是科技新聞編輯，擅長用簡短易懂的方式整理科技資訊。"
    return ask_gemini(prompt, system_instruction=instruction)


def rag_industry_advice(industry: str, articles: list[dict]) -> str:
    """RAG：根據文章內容，為指定行業生成 AI 導入建議"""
    if not articles:
        return f"目前沒有找到與 {industry} 相關的文章，請稍後再試。"

    context = "\n\n".join([
        f"【{a['title']}】\n{a['full_text'][:800]}\n來源：{a['link']}"
        for a in articles[:5]
    ])

    prompt = f"""請根據以下 TechOrange 科技報導，為「{industry}業」的台灣中小企業生成 AI 轉型建議。
要求：3 個具體可執行的建議，每項附參考文章連結，避免過度理想化，繁體中文不超過 350 字。

參考文章：
{context}
"""
    instruction = "你是企業 AI 顧問，專門幫台灣中小企業規劃 AI 導入方案。"
    return ask_gemini(prompt, system_instruction=instruction)


def explain_keyword(keyword: str, articles: list[dict]) -> str:
    """用白話文解釋科技關鍵字"""
    context = ""
    if articles:
        context = "\n\n相關報導：\n" + "\n\n".join([
            f"【{a['title']}】\n{a['excerpt']}\n來源：{a['link']}"
            for a in articles[:3]
        ])

    prompt = f"""請用「高中生都能懂的方式」解釋「{keyword}」。
格式：①一句話定義 ②生活化比喻 ③台灣應用案例 ④為什麼重要
繁體中文，不超過 250 字。{context}
"""
    instruction = "你是科技教育者，擅長把艱深的科技名詞用白話文解釋清楚。"
    return ask_gemini(prompt, system_instruction=instruction)
