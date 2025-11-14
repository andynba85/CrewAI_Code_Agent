"""
Daily Tech News Module
每日技術新聞抓取與分析功能
"""

import os
import json
import threading
import time
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from .prompt_manager import prompt_manager

load_dotenv()


def load_read_articles():
    """載入已讀文章記錄"""
    history_file = "tech_news_history.json"
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"articles": []}
    return {"articles": []}


def save_read_articles(articles_data):
    """儲存已讀文章記錄"""
    history_file = "tech_news_history.json"
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(articles_data, f, ensure_ascii=False, indent=2)


def run_daily_tech_news(
    topics: list = None,
    num_articles: int = 7,
    output_file: str = None,
    progress_callback: Optional[callable] = None
):
    """
    執行每日技術新聞抓取與分析
    
    Args:
        topics: 感興趣的主題列表（預設為 AI 相關主題）
        num_articles: 要找的文章數量（預設 7 篇）
        output_file: 輸出的報告文件名
        progress_callback: 進度回調函數
        
    Returns:
        執行結果
    """
    
    # 預設主題 - 專注於 AI 領域
    if topics is None:
        topics = [
            "Artificial Intelligence", "Machine Learning", "Deep Learning",
            "Large Language Models", "LLM", "GPT", "ChatGPT", "Generative AI",
            "Computer Vision", "Natural Language Processing", "NLP",
            "AI Agents", "AI Tools", "Neural Networks", "Transformer"
        ]
    
    # 預設輸出文件名
    if output_file is None:
        today = datetime.now().strftime("%Y%m%d")
        output_file = f"TECH_NEWS_{today}.md"
    
    # 初始化更快的 LLM
    fast_llm = LLM(
        model="gpt-4o-mini",
        temperature=0.7,
        max_tokens=5000  # 增加 token 數以支援更長的摘要
    )
    
    # 初始化工具
    search_tool = SerperDevTool()
    scrape_tool = ScrapeWebsiteTool()
    
    # 載入已讀文章
    history_data = load_read_articles()
    read_urls = [article.get('url', '') for article in history_data.get('articles', [])]
    
    # Agent 1: News Hunter (新聞獵人)
    news_hunter_backstory = """You are an expert AI and technology news curator with a keen eye for finding 
        the latest and most relevant AI/ML articles and breakthroughs. You excel at searching for recent 
        blog posts, research papers, tutorials, GitHub trending AI repositories, and AI news from reputable 
        sources like ArXiv, Hugging Face, Papers with Code, OpenAI Blog, Google AI Blog, Medium AI publications, 
        Reddit r/MachineLearning, and official AI company blogs. You know how to filter out clickbait and focus 
        on high-quality, educational content about AI that developers and researchers would find valuable."""
    
    enhanced_hunter_backstory = prompt_manager.get_enhanced_backstory(
        'DAILY_TECH_NEWS',
        'news_hunter_prompt',
        news_hunter_backstory
    )
    
    news_hunter = Agent(
        role='AI News Hunter',
        goal=f'Find {num_articles} fresh, high-quality AI/ML articles about: {", ".join(topics[:5])}',
        backstory=enhanced_hunter_backstory,
        tools=[search_tool, scrape_tool],
        llm=fast_llm,
        verbose=True,
        allow_delegation=False
    )
    
    if progress_callback:
        progress_callback("Tech News Hunter", "running", 3, 0)
    
    # Agent 2: Content Analyzer (內容分析師)
    content_analyzer_backstory = """You are an AI/ML technical content analyst who specializes in 
        reading and summarizing AI research papers and technical articles. You can quickly extract 
        key points, identify main AI concepts, model architectures, training techniques, and practical 
        applications from articles. You're skilled at creating DETAILED and COMPREHENSIVE summaries 
        that capture the essence of AI/ML content. Each summary should be at least 200-300 words to 
        provide sufficient context and insights. You also evaluate the quality and relevance of articles."""
    
    enhanced_analyzer_backstory = prompt_manager.get_enhanced_backstory(
        'DAILY_TECH_NEWS',
        'content_analyzer_prompt',
        content_analyzer_backstory
    )
    
    content_analyzer = Agent(
        role='AI Content Analyzer',
        goal='Read and analyze each AI article deeply, extract key insights and create DETAILED summaries (200-300 words each)',
        backstory=enhanced_analyzer_backstory,
        tools=[scrape_tool],
        llm=fast_llm,
        verbose=True,
        allow_delegation=False
    )
    
    # Agent 3: Report Writer (報告撰寫者)
    report_writer_backstory = """You are a skilled AI/ML technical writer who creates engaging 
        daily digests of AI news. You organize information in a clear, scannable format with proper 
        categorization, priority levels, and actionable insights. You know how to present AI/ML 
        content in a way that's both informative and easy to consume, highlighting breakthroughs, 
        new models, research findings, and practical applications."""
    
    enhanced_writer_backstory = prompt_manager.get_enhanced_backstory(
        'DAILY_TECH_NEWS',
        'report_writer_prompt',
        report_writer_backstory
    )
    
    report_writer = Agent(
        role='AI News Report Writer',
        goal='Create a well-organized daily AI/ML news digest report with detailed summaries',
        backstory=enhanced_writer_backstory,
        llm=fast_llm,
        verbose=True,
        allow_delegation=False
    )
    
    # 建立已讀 URL 列表字串
    read_urls_str = "\n".join([f"  - {url}" for url in read_urls[-50:]])  # 只顯示最近 50 筆
    if len(read_urls) > 50:
        read_urls_str += f"\n  ... 以及其他 {len(read_urls) - 50} 篇文章"
    
    # Task 1: 搜尋新文章
    search_task = Task(
        description=f"""Search for {num_articles} NEW and UNIQUE AI/Machine Learning articles published recently 
        (within the last 3-7 days) about the following AI topics: {", ".join(topics[:10])}.

IMPORTANT - FOCUS ON AI/ML CONTENT:
- Prioritize articles about AI models, ML techniques, LLMs, GenAI applications
- Include research papers, model releases, AI tool announcements
- Look for practical AI applications and case studies

IMPORTANT - AVOID DUPLICATE ARTICLES:
The following URLs have already been read and should be EXCLUDED:
{read_urls_str if read_urls else "  (No articles read yet)"}

Search Strategy:
1. Use multiple AI-focused search queries:
   - "latest AI research 2024 2025", "new LLM models", "machine learning breakthrough"
   - "generative AI applications", "AI agents", "computer vision advances"
   - "NLP innovations", "transformer models", "AI tools release"
2. Focus on reputable AI sources:
   - ArXiv.org, Papers with Code
   - Hugging Face Blog, OpenAI Blog, Google AI Blog, DeepMind Blog
   - Medium AI publications (Towards Data Science, etc.)
   - GitHub trending AI repositories
   - Reddit r/MachineLearning, r/artificial
3. For each article, provide:
   - Title
   - URL (must be NEW, not in the excluded list)
   - Source/Author
   - Publish date (if available)
   - Brief description (2-3 sentences about the AI content)

Find diverse AI articles covering different aspects of artificial intelligence.
Ensure ALL {num_articles} articles are UNIQUE and NOT in the excluded list above.
""",
        agent=news_hunter,
        expected_output=f"A list of {num_articles} unique AI/ML articles with titles, URLs, sources, and brief descriptions"
    )
    
    # Task 2: 分析文章內容
    analysis_task = Task(
        description=f"""For each AI/ML article found by the News Hunter, visit the URL and perform a detailed analysis:

1. **Read the full article** using the scrape tool
2. **Extract key AI/ML information**:
   - Main AI topic and subtopics
   - AI models, architectures, or techniques mentioned
   - Training methods, datasets, or evaluation metrics (if applicable)
   - Target audience (researcher/practitioner/beginner)
   - Key AI concepts and technologies mentioned
   - Practical applications or use cases
   - Code examples or implementations (if any)
   - Main findings and conclusions
   
3. **Create a DETAILED summary** for each article (MINIMUM 200-300 words) including:
   - Title and URL
   - **Comprehensive 200-300 word summary** explaining:
     * What the article is about
     * Key AI concepts or techniques discussed
     * Main findings or innovations
     * How it relates to current AI trends
     * Practical implications or applications
   - Key AI technologies/models covered
   - Difficulty level (beginner/intermediate/advanced)
   - Why it's valuable for AI practitioners
   - Notable implementations, code, or resources mentioned
   
4. **Rate each article** on:
   - Quality (1-5): Technical depth and accuracy
   - Relevance (1-5): How relevant to current AI trends
   - Practicality (1-5): Immediate applicability
   - Innovation (1-5): Novelty of content

IMPORTANT: Each summary must be DETAILED (200-300 words minimum) to provide sufficient context.
Analyze ALL {num_articles} articles thoroughly with comprehensive summaries.
""",
        agent=content_analyzer,
        expected_output=f"Detailed analysis and COMPREHENSIVE summaries (200-300 words each) for all {num_articles} AI articles with ratings",
        context=[search_task]
    )
    
    # Task 3: 生成每日報告
    report_task = Task(
        description=f"""Create a comprehensive daily AI/ML news digest report based on the analyzed articles.

Structure the report as follows:

# 📰 每日 AI 技術新聞摘要 - {datetime.now().strftime("%Y年%m月%d日")}

## 📊 今日統計
- 📄 文章總數：{num_articles} 篇
- 🎯 主要領域：[列出主要 AI 領域，如 LLM、Computer Vision 等]
- ⭐ 平均品質評分：[計算平均分/5]
- 🔥 熱門話題：[提取最常出現的主題]

## 🏆 今日精選推薦

For each of the TOP {min(num_articles, 5)} articles (sorted by rating), provide:

### 📌 [文章標題]

**基本資訊**
- 📝 來源：[作者/網站/出版機構]
- 🔗 連結：[完整 URL]
- 🏷️ 類別：[LLM/Computer Vision/NLP/ML/等]
- 📅 發布日期：[日期]
- 🎓 難度：⭐⭐⭐ (初級/中級/高級)
- 📊 評分：品質 ⭐⭐⭐⭐⭐ | 相關性 ⭐⭐⭐⭐ | 實用性 ⭐⭐⭐⭐⭐ | 創新性 ⭐⭐⭐⭐

**詳細摘要** (200-300 words)

[Provide a COMPREHENSIVE summary covering:]
- 文章的主要內容和核心觀點
- 討論的 AI 模型、技術或方法
- 主要發現、創新點或突破
- 實際應用場景或案例
- 與當前 AI 趨勢的關聯性
- 對讀者的價值和啟發

**關鍵技術重點**
- 🔧 技術/模型：[列出主要技術]
- 📊 方法論：[訓練方法、評估指標等]
- 💡 創新點：[新穎之處]

**實用資源**
- 📦 相關實現：[GitHub 連結、模型連結等]
- 📚 延伸閱讀：[相關論文、文章]

---

## 📚 完整文章列表

For each remaining article, provide a condensed version:

### [序號]. [文章標題]
- **來源**: [來源] | **難度**: [難度] | **評分**: ⭐⭐⭐⭐
- **摘要**: [100-150 字的簡短摘要]
- **連結**: [URL]
- **關鍵字**: [相關技術關鍵字]

---

## 🎯 本週學習建議

Based on today's articles, provide learning recommendations:

1. **優先學習主題**: [基於文章內容推薦]
   - 理由：[為什麼重要]
   - 推薦文章：[對應的文章編號]

2. **實踐項目建議**: [可以動手做的項目]
   - 相關文章：[編號]
   - 難度評估：[難度]

3. **深入研究方向**: [值得深入的領域]
   - 前景分析：[簡述]

## 🔥 技術趨勢觀察

[根據今日文章，分析當前 AI 領域的熱點趨勢]

## 📎 快速索引表

| # | 標題 | 類別 | 難度 | 評分 | 連結 |
|---|------|------|------|------|------|
| 1 | [標題簡寫] | LLM | 中級 | ⭐⭐⭐⭐ | [🔗](...) |
| 2 | [標題簡寫] | CV | 高級 | ⭐⭐⭐⭐⭐ | [🔗](...) |
| ... | ... | ... | ... | ... | ... |

---

**📅 生成時間**：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**🤖 AI Agents**: News Hunter → Content Analyzer → Report Writer

Use proper markdown formatting with emojis, headers, tables, and lists.
Make it visually appealing and easy to scan.
Save the report to: {output_file}
""",
        agent=report_writer,
        expected_output=f"A well-formatted daily AI news digest with detailed summaries saved as {output_file}",
        context=[search_task, analysis_task],
        output_file=output_file
    )
    
    # 建立 Crew
    crew = Crew(
        agents=[news_hunter, content_analyzer, report_writer],
        tasks=[search_task, analysis_task, report_task],
        process=Process.sequential,
        verbose=True
    )
    
    # 使用執行緒來模擬進度更新
    result = None
    error = None
    execution_done = threading.Event()
    
    def run_crew():
        nonlocal result, error
        try:
            result = crew.kickoff()
        except Exception as e:
            error = e
        finally:
            execution_done.set()
    
    # 啟動執行緒
    thread = threading.Thread(target=run_crew, daemon=True)
    thread.start()
    
    # 模擬進度更新（3 個 Agents，各約 33% 時間）
    if progress_callback:
        # 階段 1: News Hunter
        progress_callback("Tech News Hunter", "running", 3, 0)
        
        for i in range(50):  # 檢查 50 次，每次 2 秒
            if execution_done.is_set():
                break
            time.sleep(2)
            
            if i == 15:  # 約 33% 時間
                progress_callback("Tech News Hunter", "completed", 3, 1)
                progress_callback("Technical Content Analyzer", "running", 3, 1)
            elif i == 35:  # 約 66% 時間
                progress_callback("Technical Content Analyzer", "completed", 3, 2)
                progress_callback("Tech News Report Writer", "running", 3, 2)
    
    # 等待執行完成
    execution_done.wait()
    
    # 顯示完成
    if progress_callback:
        progress_callback("Tech News Report Writer", "completed", 3, 3)
    
    # 如果有錯誤，拋出
    if error:
        raise error
    
    # 更新已讀文章記錄（從結果中提取 URLs）
    # 注意：這裡簡化處理，實際應該從結果中解析出新的 URLs
    
    return result
