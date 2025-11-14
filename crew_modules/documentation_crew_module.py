"""
Documentation Crew Module
自動化文檔生成功能的可重用模組
"""

import os
import threading
import time
from typing import List, Union, Optional
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from .prompt_manager import prompt_manager
from .utf8_file_tool import read_files_content

load_dotenv()

def run_documentation_crew(
    target_file: Union[str, List[str]], 
    output_file: str = "OUTPUT_DOCUMENTATION.md",
    progress_callback: Optional[callable] = None
):
    """
    執行文檔生成 Crew
    
    Args:
        target_file: 要分析的代碼文件路徑（字串或列表）
        output_file: 輸出的文檔文件名
        progress_callback: 進度回調函數 (agent_name, status, total, completed)
        
    Returns:
        執行結果
    """
    # 初始化更快的 LLM（使用 gpt-4o-mini 或 gpt-3.5-turbo 更快更便宜）
    fast_llm = LLM(
        model="gpt-4o-mini",  # 更快的模型
        temperature=0.7,
        max_tokens=4000  # 限制輸出長度以加快速度
    )
    
    # 處理多個文件的情況
    if isinstance(target_file, list):
        file_list = target_file
        target_description = f"{len(file_list)} 個文件"
        file_list_str = "\n".join([f"  - {f}" for f in file_list[:10]])  # 只顯示前10個
        if len(file_list) > 10:
            file_list_str += f"\n  ... 以及其他 {len(file_list) - 10} 個文件"
    else:
        file_list = [target_file]
        target_description = target_file
        file_list_str = target_file
    
    # 預先讀取所有文件內容（避免編碼問題）
    files_content = read_files_content(file_list)
    
    # Agent 1: Senior Python Developer (Code Interpreter)
    senior_dev_backstory = """You are an expert software engineer with 15+ years of experience.
        You excel at reading complex code and understanding architecture patterns, design decisions,
        and implementation details. You can identify the purpose of each function, class, and module,
        and explain how they work together."""
    
    # 應用自訂 prompts
    enhanced_backstory = prompt_manager.get_enhanced_backstory(
        'DOCUMENTATION_CREW',
        'senior_dev_prompt',
        senior_dev_backstory
    )
    
    senior_dev = Agent(
        role='Senior Python Developer',
        goal=f'Analyze the code in {target_description} and explain its functionality in depth',
        backstory=enhanced_backstory,
        llm=fast_llm,  # 使用更快的 LLM
        verbose=True,
        allow_delegation=False
    )
    
    if progress_callback:
        progress_callback("Senior Python Developer", "running", 2, 0)
    
    # Agent 2: Technical Writer
    tech_writer_backstory = """You are a skilled technical writer who specializes in creating clear,
        structured documentation. You transform complex technical jargon into easy-to-read
        markdown documentation with proper formatting, code examples, and usage instructions.
        You follow best practices for README files including installation guides, usage examples,
        API references, and troubleshooting sections."""
    
    # 應用自訂 prompts
    enhanced_writer_backstory = prompt_manager.get_enhanced_backstory(
        'DOCUMENTATION_CREW',
        'tech_writer_prompt',
        tech_writer_backstory
    )
    
    tech_writer = Agent(
        role='Technical Documentation Writer',
        goal='Create comprehensive, user-friendly documentation based on technical analysis',
        backstory=enhanced_writer_backstory,
        llm=fast_llm,  # 使用更快的 LLM
        verbose=True,
        allow_delegation=False
    )
    
    # 將所有檔案路徑轉換為絕對路徑
    absolute_file_list = [os.path.abspath(f) for f in file_list]
    absolute_file_list_str = "\n".join([f"  - {f}" for f in absolute_file_list[:10]])
    if len(absolute_file_list) > 10:
        absolute_file_list_str += f"\n  ... 以及其他 {len(absolute_file_list) - 10} 個文件"
    
    # Task 1: Code Analysis
    # 直接在 description 中提供文件內容，避免編碼問題
    analysis_task = Task(
        description=f"""Thoroughly analyze the following code files.

Files being analyzed:
{absolute_file_list_str}

Here is the complete content of all files (already read with UTF-8 encoding):

{files_content}

Your analysis should include:
1. Overall purpose and functionality of the code
2. Main classes, functions, and their responsibilities
3. Key dependencies and imports
4. Data flow and architecture patterns
5. Any notable design decisions or algorithms used
6. Input/output expectations
7. Error handling mechanisms
8. How different files/modules work together (if multiple files)

Be detailed and technical in your analysis.
""",
        agent=senior_dev,
        expected_output="A detailed technical analysis of the code structure and functionality"
    )
    
    # Task 2: Documentation Creation
    documentation_task = Task(
        description=f"""Based on the technical analysis, create a comprehensive README.md style documentation.
        
        The documentation should include:
        
        ## 📋 Overview
        - Brief description of what the code does
        - Key features and capabilities
        
        ## 🚀 Installation
        - Dependencies required
        - Installation steps
        
        ## 💻 Usage
        - Basic usage examples with code snippets
        - Advanced usage scenarios
        - Configuration options
        
        ## 📖 API Reference
        - List of main functions/classes with parameters and return values
        - Brief description of each
        
        ## 🏗️ Architecture
        - High-level architecture explanation
        - How different components interact
        
        ## ⚠️ Important Notes
        - Any gotchas or important considerations
        - Known limitations
        
        ## 📝 Examples
        - At least 2-3 practical code examples
        
        Use proper markdown formatting with emojis, code blocks, and clear headers.
        Make it professional yet easy to understand.
        
        Save the final documentation to: {output_file}""",
        agent=tech_writer,
        expected_output=f"A complete, well-formatted markdown documentation file saved as {output_file}",
        context=[analysis_task],
        output_file=output_file
    )
    
    # 建立 Crew
    crew = Crew(
        agents=[senior_dev, tech_writer],
        tasks=[analysis_task, documentation_task],
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
    
    # 模擬進度更新
    if progress_callback:
        # 階段 1: Senior Developer (預估 50% 的時間)
        progress_callback("Senior Python Developer", "running", 2, 0)
        
        # 等待約一半時間後切換到第二個 Agent
        for i in range(30):  # 檢查 30 次，每次 2 秒 = 60 秒
            if execution_done.is_set():
                break
            time.sleep(2)
            if i == 15:  # 大約一半時間
                progress_callback("Senior Python Developer", "completed", 2, 1)
                progress_callback("Technical Documentation Writer", "running", 2, 1)
    
    # 等待執行完成
    execution_done.wait()
    
    # 顯示完成
    if progress_callback:
        progress_callback("Technical Documentation Writer", "completed", 2, 2)
    
    # 如果有錯誤，拋出
    if error:
        raise error
    
    return result
