"""
Tech Researcher Module
技術調研與決策助手功能的可重用模組
"""

import os
import threading
import time
from typing import Optional
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from .prompt_manager import prompt_manager

load_dotenv()

def run_tech_researcher(research_query: str, output_file: str = "TECH_RESEARCH_REPORT.md", progress_callback: Optional[callable] = None):
    """
    執行技術調研 Crew
    
    Args:
        research_query: 研究主題/問題
        output_file: 輸出的報告文件名
        progress_callback: 進度回調函數，用於顯示 Agent 進度
        
    Returns:
        執行結果
    """
    
    # 初始化更快的 LLM
    fast_llm = LLM(
        model="gpt-4o-mini",  # 比 gpt-4-turbo-preview 快 3-5 倍
        temperature=0.7,
        max_tokens=4000  # 限制 token 數量以提高速度
    )
    
    # 初始化工具
    search_tool = SerperDevTool()
    scrape_tool = ScrapeWebsiteTool()
    
    # Agent 1: Research Analyst (調研員)
    research_analyst_backstory = """You are an expert technology researcher with a keen eye for finding
        the most relevant and up-to-date information. You excel at searching for technical
        documentation, blog posts, GitHub repositories, Stack Overflow discussions, and
        benchmark comparisons. You know how to evaluate the credibility of sources and
        prioritize information from official documentation, reputable tech blogs, and
        recent benchmarks. You're skilled at finding both the pros and cons of technologies."""
    
    # 應用自訂 prompts
    enhanced_research_backstory = prompt_manager.get_enhanced_backstory(
        'TECH_RESEARCHER',
        'research_analyst_prompt',
        research_analyst_backstory
    )
    
    research_analyst = Agent(
        role='Tech Research Analyst',
        goal=f'Conduct comprehensive research on: {research_query}',
        backstory=enhanced_research_backstory,
        tools=[search_tool, scrape_tool],
        llm=fast_llm,  # 使用更快的 LLM
        verbose=True,
        allow_delegation=False
    )
    
    if progress_callback:
        progress_callback("Tech Research Analyst", "running", 3, 0)
    
    # Agent 2: Comparison Expert (比較專家)
    comparison_expert_backstory = """You are a technology analyst who specializes in creating detailed
        comparison matrices. You evaluate technologies across multiple dimensions including
        performance, scalability, developer experience, community support, documentation quality,
        learning curve, ecosystem maturity, and long-term viability. You present complex
        comparisons in clear, structured formats using tables and visual aids. You're objective
        and data-driven in your analysis."""
    
    # 應用自訂 prompts
    enhanced_comparison_backstory = prompt_manager.get_enhanced_backstory(
        'TECH_RESEARCHER',
        'comparison_expert_prompt',
        comparison_expert_backstory
    )
    
    comparison_expert = Agent(
        role='Technology Comparison Specialist',
        goal='Analyze and compare technologies based on multiple criteria',
        backstory=enhanced_comparison_backstory,
        llm=fast_llm,  # 使用更快的 LLM
        verbose=True,
        allow_delegation=False
    )
    
    # Agent 3: Strategy Advisor (技術長)
    strategy_advisor_backstory = """You are a seasoned CTO with 20+ years of experience making technology
        decisions for various projects. You understand that technology choices should align
        with project requirements, team expertise, timeline, and long-term maintainability.
        You consider factors like: project scale, team size, performance requirements,
        budget constraints, time to market, and future scalability. You provide clear,
        actionable recommendations backed by solid reasoning."""
    
    # 應用自訂 prompts
    enhanced_strategy_backstory = prompt_manager.get_enhanced_backstory(
        'TECH_RESEARCHER',
        'strategy_advisor_prompt',
        strategy_advisor_backstory
    )
    
    strategy_advisor = Agent(
        role='Technical Strategy Advisor (CTO)',
        goal='Provide strategic recommendations based on research and comparison',
        backstory=enhanced_strategy_backstory,
        llm=fast_llm,  # 使用更快的 LLM
        verbose=True,
        allow_delegation=False
    )
    
    # Task 1: Research and Information Gathering
    research_task = Task(
        description=f"""Conduct comprehensive research on: {research_query}
        
        Your research should gather information about:
        
        1. **Official Documentation & Resources**
           - Official websites and documentation
           - GitHub repositories (stars, activity, issues)
           - Latest version and release notes
        
        2. **Performance & Benchmarks**
           - Performance benchmarks and comparisons
           - Scalability characteristics
           - Resource consumption (memory, CPU)
        
        3. **Developer Experience**
           - Learning curve and ease of use
           - Quality of documentation
           - Available tutorials and courses
           - Development tools and IDE support
        
        4. **Community & Ecosystem**
           - Community size and activity
           - Number of contributors
           - Stack Overflow questions/answers
           - Available libraries and plugins
           - Enterprise adoption
        
        5. **Real-World Usage**
           - Companies using the technology
           - Use cases and success stories
           - Common pain points and limitations
        
        6. **Recent Trends**
           - Recent blog posts and articles (from 2024-2025)
           - Discussion on Reddit, HackerNews
           - Expert opinions and reviews
        
        Search multiple sources and compile comprehensive findings.
        Include links to sources for verification.
        """,
        agent=research_analyst,
        expected_output="A comprehensive research report with findings from multiple credible sources"
    )
    
    # Task 2: Comparison Analysis
    comparison_task = Task(
        description=f"""Based on the research findings, create a detailed comparison analysis.
        
        Create comparison tables covering:
        
        1. **Performance Comparison**
           | Metric | Technology A | Technology B | Winner |
           |--------|-------------|--------------|--------|
           | Throughput | ... | ... | ... |
           | Latency | ... | ... | ... |
           | Memory Usage | ... | ... | ... |
        
        2. **Feature Comparison**
           Compare key features, capabilities, and limitations
        
        3. **Developer Experience Comparison**
           - Learning curve (1-10 scale)
           - Documentation quality (1-10 scale)
           - Development speed
           - Debugging experience
        
        4. **Ecosystem Maturity**
           - Age of technology
           - GitHub stars/contributors
           - NPM downloads / PyPI downloads
           - Number of packages/plugins
        
        5. **Community Support**
           - Stack Overflow questions
           - Active maintainers
           - Response time for issues
        
        6. **Pros and Cons Summary**
           For each technology, list:
           ✅ Pros (strengths)
           ❌ Cons (weaknesses)
        
        7. **Use Case Fit**
           For different scenarios, which technology is better suited:
           - Small projects
           - Enterprise applications
           - High-traffic systems
           - Rapid prototyping
           - Long-term maintenance
        
        Be objective and data-driven. Include numbers and metrics where possible.
        """,
        agent=comparison_expert,
        expected_output="A structured comparison analysis with tables and clear pros/cons",
        context=[research_task]
    )
    
    # Task 3: Strategic Recommendation
    recommendation_task = Task(
        description=f"""Based on the research and comparison, provide strategic recommendations.
        
        Your report should include:
        
        ## 🎯 Executive Summary
        - Quick overview of the research question
        - Top recommendation with key reasoning (2-3 sentences)
        
        ## 📊 Research Findings Summary
        - Recap of key research findings
        - Most important data points
        
        ## ⚖️ Comparison Highlights
        - Key differences between technologies
        - Critical decision factors
        
        ## 🏆 Recommendation
        
        ### Primary Recommendation: [Technology Name]
        **Confidence Level:** [High/Medium/Low]
        
        **Why we recommend this:**
        1. Reason 1 with supporting data
        2. Reason 2 with supporting data
        3. Reason 3 with supporting data
        
        **Best suited for:**
        - Use case 1
        - Use case 2
        - Use case 3
        
        **Caveats and considerations:**
        - Important limitation or consideration 1
        - Important limitation or consideration 2
        
        ### Alternative Option: [Technology Name]
        **Consider this if:**
        - Specific scenario 1
        - Specific scenario 2
        
        ## 🚀 Implementation Roadmap
        1. **Short-term (Week 1-2):**
           - Initial steps
           - Proof of concept
        
        2. **Mid-term (Month 1-2):**
           - Development phase recommendations
        
        3. **Long-term (Month 3+):**
           - Scaling considerations
           - Optimization strategies
        
        ## 📚 Learning Resources
        - Official documentation links
        - Best tutorials/courses
        - Community resources
        
        ## ⚠️ Risk Assessment
        - Potential risks and mitigation strategies
        - Long-term maintenance considerations
        
        ## 🔗 References
        List all sources used in the research
        
        Make the recommendation clear, actionable, and well-reasoned.
        Save the complete report to: {output_file}
        """,
        agent=strategy_advisor,
        expected_output=f"A comprehensive strategic recommendation report saved as {output_file}",
        context=[research_task, comparison_task],
        output_file=output_file
    )
    
    # 建立 Crew
    crew = Crew(
        agents=[research_analyst, comparison_expert, strategy_advisor],
        tasks=[research_task, comparison_task, recommendation_task],
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
        # 階段 1: Research Analyst
        progress_callback("Tech Research Analyst", "running", 3, 0)
        
        for i in range(40):  # 檢查 40 次，每次 2 秒
            if execution_done.is_set():
                break
            time.sleep(2)
            
            if i == 12:  # 約 33% 時間
                progress_callback("Tech Research Analyst", "completed", 3, 1)
                progress_callback("Technology Comparison Specialist", "running", 3, 1)
            elif i == 25:  # 約 66% 時間
                progress_callback("Technology Comparison Specialist", "completed", 3, 2)
                progress_callback("Technical Strategy Advisor", "running", 3, 2)
    
    # 等待執行完成
    execution_done.wait()
    
    # 顯示完成
    if progress_callback:
        progress_callback("Technical Strategy Advisor", "completed", 3, 3)
    
    # 如果有錯誤，拋出
    if error:
        raise error
    
    return result
