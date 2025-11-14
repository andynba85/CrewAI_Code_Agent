"""
Refactoring Crew Module
智慧 Code Review 與重構建議功能的可重用模組
"""

import os
import threading
import time
from typing import Optional
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from .prompt_manager import prompt_manager
from .utf8_file_tool import read_files_content

load_dotenv()

def run_refactoring_crew(target_file: str, output_file: str = "REFACTORING_REPORT.md", progress_callback: Optional[callable] = None):
    """
    執行 Code Review 與重構 Crew
    
    Args:
        target_file: 要審查的代碼文件路徑
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
    
    # 預先讀取文件內容（避免編碼問題）
    abs_path = os.path.abspath(target_file)
    file_content = read_files_content([abs_path])
    
    # Agent 1: Security Auditor (資安專家)
    security_auditor_backstory = """You are a cybersecurity expert specializing in application security.
        You have deep knowledge of OWASP Top 10, common vulnerabilities like SQL injection,
        XSS, CSRF, insecure deserialization, hardcoded credentials, and other security flaws.
        You can spot security issues that developers often overlook."""
    
    # 應用自訂 prompts
    enhanced_security_backstory = prompt_manager.get_enhanced_backstory(
        'REFACTORING_CREW',
        'security_auditor_prompt',
        security_auditor_backstory
    )
    
    security_auditor = Agent(
        role='Security Auditor',
        goal=f'Identify security vulnerabilities and potential risks in {target_file}',
        backstory=enhanced_security_backstory,
        llm=fast_llm,  # 使用更快的 LLM
        verbose=True,
        allow_delegation=False
    )
    
    if progress_callback:
        progress_callback("Security Auditor", "running", 3, 0)
    
    # Agent 2: Clean Code Reviewer (代碼潔癖者)
    clean_code_reviewer_backstory = """You are a software craftsmanship advocate who lives and breathes clean code principles.
        You're an expert in SOLID principles, design patterns, naming conventions, function complexity,
        code duplication, and maintainability. You follow the teachings of Robert C. Martin (Uncle Bob),
        Martin Fowler, and other software engineering thought leaders. You believe that code should be
        self-documenting, easy to read, and a joy to maintain."""
    
    # 應用自訂 prompts
    enhanced_clean_code_backstory = prompt_manager.get_enhanced_backstory(
        'REFACTORING_CREW',
        'clean_code_reviewer_prompt',
        clean_code_reviewer_backstory
    )
    
    clean_code_reviewer = Agent(
        role='Clean Code Reviewer',
        goal='Analyze code quality, adherence to best practices, and suggest improvements',
        backstory=enhanced_clean_code_backstory,
        llm=fast_llm,  # 使用更快的 LLM
        verbose=True,
        allow_delegation=False
    )
    
    # Agent 3: Refactoring Specialist (重構專家)
    refactoring_specialist_backstory = """You are a master of code refactoring with expertise in improving code structure
        without changing its external behavior. You excel at applying design patterns, extracting methods,
        reducing complexity, and making code more maintainable. You can take raw feedback from security
        and quality reviews and translate them into actionable, well-structured code improvements."""
    
    # 應用自訂 prompts
    enhanced_refactoring_backstory = prompt_manager.get_enhanced_backstory(
        'REFACTORING_CREW',
        'refactoring_specialist_prompt',
        refactoring_specialist_backstory
    )
    
    refactoring_specialist = Agent(
        role='Refactoring Specialist',
        goal='Synthesize feedback and provide concrete refactored code with improvements',
        backstory=enhanced_refactoring_backstory,
        llm=fast_llm,  # 使用更快的 LLM
        verbose=True,
        allow_delegation=False
    )
    
    # Task 1: Security Audit
    security_task = Task(
        description=f"""Perform a comprehensive security audit on the following code file.

File: {abs_path}

Here is the complete content (already read with UTF-8 encoding):

{file_content}

Check for:
1. **Hardcoded Secrets**: API keys, passwords, tokens embedded in code
2. **SQL Injection**: Unsafe SQL query construction
3. **Command Injection**: Unsafe use of os.system, subprocess, eval
4. **Path Traversal**: Improper file path handling
5. **Insecure Deserialization**: Unsafe pickle, yaml.load usage
6. **Weak Cryptography**: Use of MD5, SHA1, weak encryption
7. **Input Validation**: Missing or insufficient input validation
8. **Error Handling**: Information leakage in error messages
9. **Authentication/Authorization**: Weak or missing security checks
10. **Dependency Vulnerabilities**: Known vulnerable dependencies

For each issue found, provide:
- Severity level (Critical/High/Medium/Low)
- Description of the vulnerability
- Potential impact
- Line numbers (if applicable)
""",
        agent=security_auditor,
        expected_output="A detailed security audit report with categorized vulnerabilities"
    )
    
    # Task 2: Code Quality Review
    quality_task = Task(
        description=f"""Perform a thorough code quality review on the following code file.

File: {abs_path}

Code content (already provided above in the security task context).

Analyze:
        1. **Naming Conventions**: Variable, function, class names clarity and consistency
        2. **Function Length**: Functions should be short and focused (ideally < 20 lines)
        3. **Complexity**: Cyclomatic complexity, nested loops/conditions
        4. **Code Duplication**: Repeated code blocks (DRY principle)
        5. **SOLID Principles**:
           - Single Responsibility Principle
           - Open/Closed Principle
           - Liskov Substitution Principle
           - Interface Segregation Principle
           - Dependency Inversion Principle
        6. **Code Smells**:
           - Long parameter lists
           - God objects/classes
           - Feature envy
           - Inappropriate intimacy
        7. **Documentation**: Missing docstrings, unclear comments
        8. **Error Handling**: Proper exception handling
        9. **Type Hints**: Usage of Python type annotations
        10. **Code Organization**: Logical structure and separation of concerns
        
        For each issue, provide:
        - Category (e.g., "Naming", "Complexity")
        - Description
        - Impact on maintainability
        - Suggested improvement
        """,
        agent=clean_code_reviewer,
        expected_output="A comprehensive code quality report with improvement suggestions"
    )
    
    # Task 3: Refactoring and Improvement
    refactoring_task = Task(
        description=f"""Based on the security audit and code quality review, create a comprehensive
        refactoring report with improved code.
        
        Your report should include:
        
        ## 🔍 Executive Summary
        - Overview of findings
        - Priority issues to address
        - Estimated refactoring effort
        
        ## 🚨 Critical Issues (Must Fix)
        List all critical security vulnerabilities and major code quality issues
        
        ## ⚠️ Important Improvements (Should Fix)
        List medium priority issues
        
        ## 💡 Nice-to-Have Enhancements (Could Fix)
        List low priority improvements
        
        ## ✨ Refactored Code
        Provide the complete refactored version of the code with:
        - All critical security issues fixed
        - Improved naming and structure
        - Better error handling
        - Added type hints
        - Comprehensive docstrings
        - Comments explaining key improvements
        
        ## 📊 Before/After Comparison
        Show side-by-side comparisons of key improvements
        
        ## 🎯 Key Improvements Made
        Summarize the main refactoring changes and their benefits
        
        ## 🧪 Testing Recommendations
        Suggest test cases to verify the refactored code
        
        Use proper markdown formatting with code blocks, tables, and clear sections.
        Save the report to: {output_file}
        """,
        agent=refactoring_specialist,
        expected_output=f"A complete refactoring report with improved code saved as {output_file}",
        context=[security_task, quality_task],
        output_file=output_file
    )
    
    # 建立 Crew
    crew = Crew(
        agents=[security_auditor, clean_code_reviewer, refactoring_specialist],
        tasks=[security_task, quality_task, refactoring_task],
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
        # 階段 1: Security Auditor
        progress_callback("Security Auditor", "running", 3, 0)
        
        for i in range(40):  # 檢查 40 次，每次 2 秒
            if execution_done.is_set():
                break
            time.sleep(2)
            
            if i == 12:  # 約 33% 時間
                progress_callback("Security Auditor", "completed", 3, 1)
                progress_callback("Clean Code Reviewer", "running", 3, 1)
            elif i == 25:  # 約 66% 時間
                progress_callback("Clean Code Reviewer", "completed", 3, 2)
                progress_callback("Refactoring Specialist", "running", 3, 2)
    
    # 等待執行完成
    execution_done.wait()
    
    # 顯示完成
    if progress_callback:
        progress_callback("Refactoring Specialist", "completed", 3, 3)
    
    # 如果有錯誤，拋出
    if error:
        raise error
    
    return result
