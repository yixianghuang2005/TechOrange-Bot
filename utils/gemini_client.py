"""
Gemini API 封裝
上課寫法：from google import genai + client.models.generate_content()
環境變數名稱：GEMINI_API_KEY
"""
from google import genai
from google.genai import types

MODEL = "gemini-2.5-flash"


def _get_client():
    """每次呼叫才建立 client，確保能讀到環境變數"""
    import os
    api_key = os.getenv("GEMINI_API_KEY")
    return genai.Client(api_key=api_key)


def ask_gemini(prompt: str, system_instruction: str = None) -> str:
    try:
        client = _get_client()
        if system_instruction:
            config = types.GenerateContentConfig(
                max_output_tokens=500,
                system_instruction=system_instruction
            )
            response = client.models.generate_content(
                model=MODEL, contents=prompt, config=config
            )
        else:
            response = client.models.generate_content(
                model=MODEL, contents=prompt
            )
        return response.text if response.text else "抱歉，AI 暫時無法回應，請稍後再試。"
    except Exception as e:
        return f"⚠️ AI 暫時無法回應：{str(e)}"


def summarize_articles(articles: list) -> str:
    if not articles:
        return "目前暫無最新文章。"
    article_text = "\n\n".join([
        f"標題：{a['title']}\n摘要：{a['excerpt']}" for a in articles
    ])
    prompt = f"""請將以下 TechOrange 文章整理成「30 秒科技早報」。
格式：每篇用「📌 標題 + 一句精華重點」呈現，最後加「📎 今日關鍵詞：xxx、xxx」
全部繁體中文，不超過 300 字。\n\n{article_text}"""
    return ask_gemini(prompt, system_instruction="你是科技新聞編輯，擅長整理科技資訊。")


def rag_industry_advice(industry: str, articles: list) -> str:
    if not articles:
        return f"目前沒有找到與 {industry} 相關的文章，請稍後再試。"
    context = "\n\n".join([
        f"【{a['title']}】\n{a['full_text'][:800]}\n來源：{a['link']}"
        for a in articles[:5]
    ])
    prompt = f"""請根據以下 TechOrange 科技報導，為「{industry}業」的台灣中小企業生成 AI 轉型建議。
要求：3 個具體可執行的建議，每項附參考文章連結，繁體中文不超過 350 字。\n\n{context}"""
    return ask_gemini(prompt, system_instruction="你是企業 AI 顧問，專門幫台灣中小企業規劃 AI 導入方案。")


def explain_keyword(keyword: str, articles: list) -> str:
    context = ""
    if articles:
        context = "\n\n相關報導：\n" + "\n\n".join([
            f"【{a['title']}】\n{a['excerpt']}\n來源：{a['link']}"
            for a in articles[:3]
        ])
    prompt = f"""請用「高中生都能懂的方式」解釋「{keyword}」。
格式：①一句話定義 ②生活化比喻 ③台灣應用案例 ④為什麼重要
繁體中文，不超過 250 字。{context}"""
    return ask_gemini(prompt, system_instruction="你是科技教育者，擅長把艱深名詞用白話文解釋清楚。")
