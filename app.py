"""
CrewAI Code Agent - Streamlit Web UI
提供友善的網頁介面來操作三個 CrewAI 應用
"""

import os
import sys
from datetime import datetime

# 🔇 停用 CrewAI 遙測，避免連線錯誤訊息
os.environ['OTEL_SDK_DISABLED'] = 'true'

import streamlit as st
from streamlit_option_menu import option_menu
from pathlib import Path

# 🔐 導入認證模組
from auth_manager import require_authentication, show_user_info

# 設定頁面配置
st.set_page_config(
    page_title="CrewAI Code Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自訂 CSS
st.markdown("""
<style>
    /* 加寬 Sidebar */
    [data-testid="stSidebar"] {
        min-width: 320px;
        max-width: 320px;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1E88E5;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #E8F5E9;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4CAF50;
        margin-bottom: 1rem;
    }
    .warning-box {
        background-color: #FFF3E0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #FF9800;
        margin-bottom: 1rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 檢查環境變數
def check_api_keys():
    """檢查必要的 API Keys 是否設定"""
    from dotenv import load_dotenv
    load_dotenv()
    
    openai_key = os.getenv('OPENAI_API_KEY')
    serper_key = os.getenv('SERPER_API_KEY')
    
    return {
        'openai': bool(openai_key and openai_key != 'your_openai_api_key_here'),
        'serper': bool(serper_key and serper_key != 'your_serper_api_key_here')
    }

# 主頁
def show_home():
    st.markdown('<div class="main-header">🤖 CrewAI Code Agent</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h3>👋 歡迎使用 AI 驅動的開發助手！</h3>
        <p>這是一個基於 CrewAI 框架的智能開發助手集合，透過多個 AI Agent 協作完成複雜任務。</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 檢查 API Keys
    api_status = check_api_keys()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if api_status['openai']:
            st.success("✅ OpenAI API Key 已設定")
        else:
            st.error("❌ OpenAI API Key 未設定（必需）")
            st.info("請在 .env 文件中設定 OPENAI_API_KEY")
    
    with col2:
        if api_status['serper']:
            st.success("✅ Serper API Key 已設定")
        else:
            st.warning("⚠️ Serper API Key 未設定（選用，僅 Tech Researcher 需要）")
    
    st.markdown("---")
    
    # 功能介紹
    st.markdown('<div class="sub-header">🎯 四大核心功能</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📖 Documentation Crew
        **自動化文檔生成**
        
        - 🔍 深度代碼分析
        - ✍️ 自動生成 README
        - 📊 架構說明
        - 💡 使用範例
        
        **適合：** 補文檔、理解代碼、API 文檔
        """)
        
        st.markdown("""
        ### 🔍 Tech Researcher
        **技術調研助手**
        
        - 🌐 網路資訊搜尋
        - ⚖️ 優劣勢比較
        - 🎯 決策建議
        - 📊 實施路線圖
        
        **適合：** 技術選型、學習新技術、工具評估
        """)
    
    with col2:
        st.markdown("""
        ### 🔧 Refactoring Crew
        **智慧 Code Review**
        
        - 🛡️ 安全漏洞掃描
        - 🧹 代碼品質檢查
        - ♻️ 重構建議
        - ✨ 優化後代碼
        
        **適合：** Code Review、安全檢查、重構
        """)
        
        st.markdown("""
        ### 📰 每日技術新聞 ✨NEW
        **自動新聞摘要**
        
        - 🔍 搜尋最新 AI 技術文章（不重複）
        - 📖 深度內容分析與摘要
        - ⭐ 智能評分推薦
        - 📝 結構化每日報告
        
        **AI Agents**：
        - 🕵️ Tech News Hunter - 搜尋最新技術文章
        - 📊 Content Analyzer - 深度分析與摘要
        - ✍️ Report Writer - 生成每日報告
        
        **適合：** 追蹤 AI 趨勢、持續學習
        """)
    
    st.markdown("---")
    
    # 快速開始
    st.markdown('<div class="sub-header">🚀 快速開始</div>', unsafe_allow_html=True)
    
    st.markdown("""
    1. **設定 API Key**：確保 `.env` 文件中已設定 `OPENAI_API_KEY`
    2. **選擇功能**：從左側選單選擇你要使用的功能
    3. **輸入資訊**：依照指示輸入必要資訊
    4. **開始執行**：點擊按鈕開始執行，等待 AI Agents 完成工作
    5. **查看結果**：下載或查看生成的報告
    
    💡 **提示**：第一次執行可能需要 3-10 分鐘，請耐心等待。
    """)

# Documentation Crew 頁面
def show_documentation_crew():
    st.markdown('<div class="main-header">📖 Documentation Crew</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">自動化文檔生成小隊</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h4>🎭 AI Agents 團隊：</h4>
        <ul>
            <li><strong>Senior Python Developer</strong>：深度分析代碼結構與邏輯</li>
            <li><strong>Technical Writer</strong>：撰寫易讀的技術文檔</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # 檢查 API Key
    api_status = check_api_keys()
    if not api_status['openai']:
        st.error("❌ 請先在 .env 文件中設定 OPENAI_API_KEY")
        return
    
    # 歷史紀錄區域
    from crew_modules.history_manager import history_manager
    
    with st.expander("📚 歷史紀錄", expanded=False):
        history_records = history_manager.get_history('documentation', limit=10)
        
        if history_records:
            for record in history_records:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    timestamp = history_manager.format_timestamp(record['timestamp'])
                    status_icon = "✅" if record.get('success') else "❌"
                    file_count = len(record.get('input_files', []))
                    st.markdown(f"{status_icon} **{timestamp}** - {file_count} 個檔案")
                
                with col2:
                    if record.get('file_exists') and record.get('output_file'):
                        if st.button("📄 查看", key=f"view_{record['id']}"):
                            try:
                                with open(record['output_file'], 'r', encoding='utf-8') as f:
                                    content = f.read()
                                st.session_state['viewing_doc'] = {
                                    'content': content,
                                    'filename': record['output_file']
                                }
                            except Exception as e:
                                st.error(f"無法讀取檔案：{e}")
                    else:
                        st.text("檔案不存在")
                
                with col3:
                    if st.button("🗑️", key=f"del_{record['id']}"):
                        history_manager.delete_record(record['id'])
                        st.rerun()
            
            if st.button("🗑️ 清除全部歷史"):
                history_manager.clear_history('documentation')
                st.rerun()
        else:
            st.info("尚無歷史紀錄")
    
    # 顯示正在查看的文檔
    if 'viewing_doc' in st.session_state:
        st.markdown("---")
        st.markdown(f"### 📄 {st.session_state['viewing_doc']['filename']}")
        st.markdown(st.session_state['viewing_doc']['content'])
        
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("❌ 關閉"):
                del st.session_state['viewing_doc']
                st.rerun()
        with col2:
            st.download_button(
                label="📥 下載",
                data=st.session_state['viewing_doc']['content'],
                file_name=Path(st.session_state['viewing_doc']['filename']).name,
                mime="text/markdown"
            )
        st.markdown("---")
    
    # 輸入區
    st.markdown("### 📂 選擇要分析的代碼")
    
    # 輸入模式選擇
    input_mode = st.radio(
        "選擇輸入模式：",
        ["視窗選擇（推薦）", "手動輸入路徑", "上傳文件"],
        horizontal=True
    )
    
    file_paths = []
    
    if input_mode == "視窗選擇（推薦）":
        st.markdown("""
        <div class="info-box">
            <small>💡 點擊按鈕會開啟檔案選擇視窗<br>
            可以選擇多個檔案或整個目錄<br>
            系統會自動跳過敏感文件（如 .env, credentials.json 等）</small>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📁 選擇檔案", type="secondary", use_container_width=True):
                from crew_modules.file_picker import pick_multiple_files
                selected_files = pick_multiple_files(
                    title="選擇 Python 檔案",
                    filetypes=[("Python files", "*.py"), ("All files", "*.*")]
                )
                if selected_files:
                    st.session_state['selected_files'] = selected_files
                    st.rerun()
        
        with col2:
            if st.button("📂 選擇目錄", type="secondary", use_container_width=True):
                from crew_modules.file_picker import pick_directory
                from crew_modules.file_utils import scan_directory_for_python_files
                
                selected_dir = pick_directory(title="選擇目錄")
                if selected_dir:
                    valid_files, excluded_files = scan_directory_for_python_files(
                        selected_dir,
                        recursive=True,
                        exclude_sensitive=True
                    )
                    st.session_state['selected_files'] = valid_files
                    st.session_state['excluded_files'] = excluded_files
                    st.rerun()
        
        # 顯示已選擇的檔案
        if 'selected_files' in st.session_state and st.session_state['selected_files']:
            from crew_modules.file_utils import format_file_list
            
            file_paths = st.session_state['selected_files']
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("✅ 已選擇檔案", len(file_paths))
            with col2:
                excluded_count = len(st.session_state.get('excluded_files', []))
                st.metric("🔒 已排除敏感檔案", excluded_count)
            
            with st.expander(f"📄 查看 {len(file_paths)} 個檔案", expanded=True):
                st.text(format_file_list(file_paths, max_display=50))
            
            if 'excluded_files' in st.session_state and st.session_state['excluded_files']:
                with st.expander(f"🔒 查看 {excluded_count} 個已排除的敏感檔案", expanded=False):
                    st.text(format_file_list(st.session_state['excluded_files'], max_display=50))
            
            if st.button("🗑️ 清除選擇"):
                if 'selected_files' in st.session_state:
                    del st.session_state['selected_files']
                if 'excluded_files' in st.session_state:
                    del st.session_state['excluded_files']
                st.rerun()
    
    elif input_mode == "手動輸入路徑":
        st.markdown("""
        <div class="info-box">
            <small>💡 提示：每行輸入一個路徑（文件或目錄）<br>
            目錄會自動遞迴掃描所有 .py 文件<br>
            系統會自動跳過敏感文件（如 .env, credentials.json 等）</small>
        </div>
        """, unsafe_allow_html=True)
        
        paths_input = st.text_area(
            "輸入多個路徑（每行一個）",
            value="./crew_modules\n./example_code.py",
            height=150,
            help="可以是文件或目錄路徑，每行一個"
        )
        
        if paths_input:
            from crew_modules.file_utils import scan_multiple_paths, format_file_list
            
            input_paths = [p.strip() for p in paths_input.split('\n') if p.strip()]
            valid_files, excluded_files = scan_multiple_paths(
                input_paths, 
                recursive=True, 
                exclude_sensitive=True
            )
            
            # 顯示掃描結果
            col1, col2 = st.columns(2)
            with col1:
                st.metric("✅ 有效文件", len(valid_files))
            with col2:
                st.metric("🔒 已排除敏感文件", len(excluded_files))
            
            if valid_files:
                with st.expander(f"📄 查看 {len(valid_files)} 個有效文件"):
                    st.text(format_file_list(valid_files, max_display=50))
            
            if excluded_files:
                with st.expander(f"🔒 查看 {len(excluded_files)} 個已排除的敏感文件", expanded=False):
                    st.text(format_file_list(excluded_files, max_display=50))
            
            file_paths = valid_files
    
    else:  # 上傳文件
        uploaded_file = st.file_uploader("上傳 Python 文件", type=['py'])
        if uploaded_file:
            file_path = f"temp_{uploaded_file.name}"
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"✅ 文件已上傳：{file_path}")
            file_paths = [file_path]
    
    # 執行按鈕
    st.markdown("---")
    
    if st.button("🚀 開始生成文檔", type="primary"):
        if not file_paths:
            st.error("❌ 請先選擇要分析的文件")
            return
        
        # 創建進度顯示容器
        progress_container = st.empty()
        status_container = st.container()
        
        # 定義進度回調函數
        def update_progress(agent_name, status, total_agents, completed_agents):
            with progress_container:
                if status == "running":
                    st.progress(completed_agents / total_agents, f"🔄 {agent_name} 正在執行...")
                elif status == "completed":
                    st.progress(completed_agents / total_agents, f"✅ {agent_name} 已完成 ({completed_agents}/{total_agents})")
            
        with st.spinner("🤖 AI Agents 正在工作中... 這可能需要幾分鐘"):
            try:
                # 動態導入
                from crew_modules import documentation_crew_module
                
                # 根據文件數量決定輸出文件名
                if len(file_paths) == 1:
                    output_file = f"DOCS_{Path(file_paths[0]).stem}.md"
                else:
                    output_file = f"DOCS_MultiFile_{len(file_paths)}files.md"
                
                # 執行 Crew（傳入文件列表或單個文件）
                target = file_paths if len(file_paths) > 1 else file_paths[0]
                result = documentation_crew_module.run_documentation_crew(
                    target, 
                    output_file,
                    progress_callback=update_progress
                )
                
                # 記錄到歷史
                history_manager.add_record(
                    crew_type='documentation',
                    input_files=file_paths,
                    output_file=output_file,
                    success=True
                )
                
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.markdown("### ✅ 文檔生成完成！")
                st.markdown(f"**分析文件數量**：{len(file_paths)}")
                st.markdown(f"**輸出文件**：`{output_file}`")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # 顯示結果
                if os.path.exists(output_file):
                    with open(output_file, 'r', encoding='utf-8') as f:
                        doc_content = f.read()
                    
                    st.markdown("### 📄 生成的文檔預覽")
                    st.markdown(doc_content)
                    
                    # 下載按鈕
                    st.download_button(
                        label="📥 下載文檔",
                        data=doc_content,
                        file_name=output_file,
                        mime="text/markdown"
                    )
                
            except Exception as e:
                # 記錄錯誤到歷史
                history_manager.add_record(
                    crew_type='documentation',
                    input_files=file_paths,
                    output_file=output_file if 'output_file' in locals() else None,
                    success=False,
                    error_message=str(e)
                )
                
                st.error(f"❌ 執行錯誤：{str(e)}")
                st.exception(e)

# Refactoring Crew 頁面
def show_refactoring_crew():
    st.markdown('<div class="main-header">🔧 Refactoring Crew</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">智慧 Code Review 與重構建議</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h4>🎭 AI Agents 團隊：</h4>
        <ul>
            <li><strong>Security Auditor</strong>：掃描安全漏洞（SQL Injection, XSS, 硬編碼密鑰等）</li>
            <li><strong>Clean Code Reviewer</strong>：檢查代碼品質（SOLID 原則、命名規範、複雜度）</li>
            <li><strong>Refactoring Specialist</strong>：提供重構後的優化代碼</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # 檢查 API Key
    api_status = check_api_keys()
    if not api_status['openai']:
        st.error("❌ 請先在 .env 文件中設定 OPENAI_API_KEY")
        return
    
    # 歷史紀錄區域
    from crew_modules.history_manager import history_manager
    
    with st.expander("� 歷史紀錄", expanded=False):
        history_records = history_manager.get_history('refactoring', limit=10)
        
        if history_records:
            for record in history_records:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    timestamp = history_manager.format_timestamp(record['timestamp'])
                    status_icon = "✅" if record.get('success') else "❌"
                    file_count = len(record.get('input_files', []))
                    st.markdown(f"{status_icon} **{timestamp}** - {file_count} 個檔案")
                
                with col2:
                    if record.get('file_exists') and record.get('output_file'):
                        if st.button("📄 查看", key=f"view_ref_{record['id']}"):
                            try:
                                with open(record['output_file'], 'r', encoding='utf-8') as f:
                                    content = f.read()
                                st.session_state['viewing_refactor_doc'] = {
                                    'content': content,
                                    'filename': record['output_file']
                                }
                            except Exception as e:
                                st.error(f"無法讀取檔案：{e}")
                    else:
                        st.text("檔案不存在")
                
                with col3:
                    if st.button("🗑️", key=f"del_ref_{record['id']}"):
                        history_manager.delete_record(record['id'])
                        st.rerun()
            
            if st.button("🗑️ 清除全部歷史", key="clear_refactor_history"):
                history_manager.clear_history('refactoring')
                st.rerun()
        else:
            st.info("尚無歷史紀錄")
    
    # 顯示正在查看的文檔
    if 'viewing_refactor_doc' in st.session_state:
        st.markdown("---")
        st.markdown(f"### 📄 {st.session_state['viewing_refactor_doc']['filename']}")
        st.markdown(st.session_state['viewing_refactor_doc']['content'])
        
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("❌ 關閉", key="close_refactor_doc"):
                del st.session_state['viewing_refactor_doc']
                st.rerun()
        with col2:
            st.download_button(
                label="📥 下載",
                data=st.session_state['viewing_refactor_doc']['content'],
                file_name=Path(st.session_state['viewing_refactor_doc']['filename']).name,
                mime="text/markdown",
                key="download_refactor_doc"
            )
        st.markdown("---")
    
    # 輸入區
    st.markdown("### 📂 選擇要審查的代碼")
    
    # 輸入模式選擇
    input_mode = st.radio(
        "選擇輸入模式：",
        ["視窗選擇（推薦）", "手動輸入路徑", "上傳文件"],
        horizontal=True,
        key="refactor_input_mode"
    )
    
    file_paths = []
    
    if input_mode == "視窗選擇（推薦）":
        st.markdown("""
        <div class="info-box">
            <small>💡 點擊按鈕會開啟檔案選擇視窗<br>
            可以選擇多個檔案或整個目錄<br>
            系統會自動跳過敏感文件（如 .env, credentials.json 等）</small>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📁 選擇檔案", type="secondary", use_container_width=True, key="refactor_pick_files"):
                from crew_modules.file_picker import pick_multiple_files
                selected_files = pick_multiple_files(
                    title="選擇 Python 檔案",
                    filetypes=[("Python files", "*.py"), ("All files", "*.*")]
                )
                if selected_files:
                    st.session_state['refactor_selected_files'] = selected_files
                    st.rerun()
        
        with col2:
            if st.button("📂 選擇目錄", type="secondary", use_container_width=True, key="refactor_pick_dir"):
                from crew_modules.file_picker import pick_directory
                from crew_modules.file_utils import scan_directory_for_python_files
                
                selected_dir = pick_directory(title="選擇目錄")
                if selected_dir:
                    valid_files, excluded_files = scan_directory_for_python_files(
                        selected_dir,
                        recursive=True,
                        exclude_sensitive=True
                    )
                    st.session_state['refactor_selected_files'] = valid_files
                    st.session_state['refactor_excluded_files'] = excluded_files
                    st.rerun()
        
        # 顯示已選擇的檔案
        if 'refactor_selected_files' in st.session_state and st.session_state['refactor_selected_files']:
            from crew_modules.file_utils import format_file_list
            
            file_paths = st.session_state['refactor_selected_files']
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("✅ 已選擇檔案", len(file_paths))
            with col2:
                excluded_count = len(st.session_state.get('refactor_excluded_files', []))
                st.metric("🔒 已排除敏感檔案", excluded_count)
            
            with st.expander(f"📄 查看 {len(file_paths)} 個檔案", expanded=True):
                st.text(format_file_list(file_paths, max_display=50))
            
            if 'refactor_excluded_files' in st.session_state and st.session_state['refactor_excluded_files']:
                with st.expander(f"🔒 查看 {excluded_count} 個已排除的敏感檔案", expanded=False):
                    st.text(format_file_list(st.session_state['refactor_excluded_files'], max_display=50))
            
            if st.button("🗑️ 清除選擇", key="refactor_clear_selection"):
                if 'refactor_selected_files' in st.session_state:
                    del st.session_state['refactor_selected_files']
                if 'refactor_excluded_files' in st.session_state:
                    del st.session_state['refactor_excluded_files']
                st.rerun()
    
    elif input_mode == "手動輸入路徑":
        file_path = st.text_input(
            "代碼文件路徑",
            value="example_code.py",
            help="輸入要審查的 Python 文件路徑",
            key="refactor_manual_path"
        )
        if file_path and os.path.exists(file_path):
            file_paths = [file_path]
    
    else:  # 上傳文件
        uploaded_file = st.file_uploader("上傳 Python 文件", type=['py'], key="refactor_upload_file")
        if uploaded_file:
            file_path = f"temp_{uploaded_file.name}"
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"✅ 文件已上傳：{file_path}")
            file_paths = [file_path]
    
    # 執行按鈕
    st.markdown("---")
    
    if st.button("🔍 開始 Code Review", type="primary"):
        if not file_paths:
            st.error("❌ 請先選擇要審查的文件")
            return
        
        # 創建進度顯示容器
        progress_container = st.empty()
        
        # 定義進度回調函數
        def update_progress(agent_name, status, total_agents, completed_agents):
            with progress_container:
                if status == "running":
                    st.progress(completed_agents / total_agents, f"🔄 {agent_name} 正在執行...")
                elif status == "completed":
                    st.progress(completed_agents / total_agents, f"✅ {agent_name} 已完成 ({completed_agents}/{total_agents})")
        
        with st.spinner("🤖 AI Agents 正在審查代碼... 這可能需要 5-10 分鐘"):
            try:
                # 動態導入
                from crew_modules import refactoring_crew_module
                
                # 根據文件數量決定輸出文件名
                if len(file_paths) == 1:
                    output_file = f"REFACTORING_{Path(file_paths[0]).stem}.md"
                    target = file_paths[0]
                else:
                    output_file = f"REFACTORING_MultiFile_{len(file_paths)}files.md"
                    target = file_paths[0]  # 目前只支援單檔案，多檔案需要修改模組
                
                # 執行 Crew
                result = refactoring_crew_module.run_refactoring_crew(
                    target, 
                    output_file,
                    progress_callback=update_progress
                )
                
                # 記錄到歷史
                history_manager.add_record(
                    crew_type='refactoring',
                    input_files=file_paths,
                    output_file=output_file,
                    success=True
                )
                
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.markdown("### ✅ Code Review 完成！")
                st.markdown(f"**分析文件數量**：{len(file_paths)}")
                st.markdown(f"**輸出報告**：`{output_file}`")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # 顯示結果
                if os.path.exists(output_file):
                    with open(output_file, 'r', encoding='utf-8') as f:
                        report_content = f.read()
                    
                    st.markdown("### 📊 審查報告預覽")
                    st.markdown(report_content)
                    
                    # 下載按鈕
                    st.download_button(
                        label="📥 下載報告",
                        data=report_content,
                        file_name=output_file,
                        mime="text/markdown",
                        key="download_refactor_report"
                    )
                
            except Exception as e:
                # 記錄錯誤到歷史
                history_manager.add_record(
                    crew_type='refactoring',
                    input_files=file_paths,
                    output_file=output_file if 'output_file' in locals() else None,
                    success=False,
                    error_message=str(e)
                )
                
                st.error(f"❌ 執行錯誤：{str(e)}")
                st.exception(e)

# Tech Researcher 頁面
def show_tech_researcher():
    st.markdown('<div class="main-header">🔍 Tech Stack Researcher</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">技術調研與決策助手</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h4>🎭 AI Agents 團隊：</h4>
        <ul>
            <li><strong>Research Analyst</strong>：搜尋最新技術資訊、文檔、基準測試</li>
            <li><strong>Comparison Expert</strong>：建立詳細的比較分析表</li>
            <li><strong>Strategy Advisor (CTO)</strong>：基於分析給出戰略建議</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # 檢查 API Keys
    api_status = check_api_keys()
    if not api_status['openai']:
        st.error("❌ 請先在 .env 文件中設定 OPENAI_API_KEY")
        return
    
    if not api_status['serper']:
        st.markdown("""
        <div class="warning-box">
            ⚠️ <strong>未設定 Serper API Key</strong><br>
            此功能可以運作，但 Agent 將只使用 LLM 的既有知識，無法搜尋最新的網路資訊。<br>
            建議前往 <a href="https://serper.dev" target="_blank">serper.dev</a> 註冊並取得免費 API Key。
        </div>
        """, unsafe_allow_html=True)
    
    # 歷史紀錄區域
    from crew_modules.history_manager import history_manager
    
    with st.expander("📚 歷史紀錄", expanded=False):
        history_records = history_manager.get_history('research', limit=10)
        
        if history_records:
            for record in history_records:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    timestamp = history_manager.format_timestamp(record['timestamp'])
                    status_icon = "✅" if record.get('success') else "❌"
                    # 顯示問題預覽（取前50個字符）
                    query_preview = record.get('input_files', [''])[0][:50] + "..." if len(record.get('input_files', [''])[0]) > 50 else record.get('input_files', [''])[0]
                    st.markdown(f"{status_icon} **{timestamp}**<br><small>{query_preview}</small>", unsafe_allow_html=True)
                
                with col2:
                    if record.get('file_exists') and record.get('output_file'):
                        if st.button("📄 查看", key=f"view_res_{record['id']}"):
                            try:
                                with open(record['output_file'], 'r', encoding='utf-8') as f:
                                    content = f.read()
                                st.session_state['viewing_research_doc'] = {
                                    'content': content,
                                    'filename': record['output_file'],
                                    'query': record.get('input_files', [''])[0]
                                }
                            except Exception as e:
                                st.error(f"無法讀取檔案：{e}")
                    else:
                        st.text("檔案不存在")
                
                with col3:
                    if st.button("🗑️", key=f"del_res_{record['id']}"):
                        history_manager.delete_record(record['id'])
                        st.rerun()
            
            if st.button("🗑️ 清除全部歷史", key="clear_research_history"):
                history_manager.clear_history('research')
                st.rerun()
        else:
            st.info("尚無歷史紀錄")
    
    # 顯示正在查看的文檔
    if 'viewing_research_doc' in st.session_state:
        st.markdown("---")
        st.markdown(f"### 📄 {st.session_state['viewing_research_doc']['filename']}")
        st.markdown(f"**問題：** {st.session_state['viewing_research_doc']['query']}")
        st.markdown("---")
        st.markdown(st.session_state['viewing_research_doc']['content'])
        
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("❌ 關閉", key="close_research_doc"):
                del st.session_state['viewing_research_doc']
                st.rerun()
        with col2:
            st.download_button(
                label="📥 下載",
                data=st.session_state['viewing_research_doc']['content'],
                file_name=Path(st.session_state['viewing_research_doc']['filename']).name,
                mime="text/markdown",
                key="download_research_doc"
            )
        st.markdown("---")
    
    # 輸入區
    st.markdown("### 🔍 輸入技術調研問題")
    
    # 輸入模式選擇
    input_mode = st.radio(
        "選擇輸入方式：",
        ["自訂問題", "從範例選擇"],
        horizontal=True,
        key="research_input_mode"
    )
    
    research_query = ""
    
    if input_mode == "自訂問題":
        st.markdown("""
        <div class="info-box">
            <small>💡 提示：請清楚描述你的技術選型需求或比較問題<br>
            建議包含：使用場景、技術選項、關注重點（性能、易用性、生態系統等）</small>
        </div>
        """, unsafe_allow_html=True)
        
        research_query = st.text_area(
            "輸入你的研究問題",
            value="",
            height=150,
            placeholder="例如：比較 FastAPI 和 Django Channels 用於高併發的即時聊天應用，重點分析性能、開發效率和擴展性",
            help="清楚描述你的技術選型需求或比較問題",
            key="research_custom_query"
        )
    
    else:  # 從範例選擇
        st.markdown("""
        <div class="info-box">
            <small>💡 從下方選擇一個範例問題，或點擊後修改成你的需求</small>
        </div>
        """, unsafe_allow_html=True)
        
        example_questions = [
            "比較 FastAPI 和 Django Channels 用於高併發的即時聊天應用",
            "評估 Next.js 和 Remix 用於建立 SEO 友好的電商網站",
            "分析 PostgreSQL vs MongoDB 用於社交媒體應用的優劣",
            "比較 React 和 Vue.js 用於企業後台管理系統",
            "評估 Docker Swarm 和 Kubernetes 用於微服務部署",
            "比較 SQLAlchemy 和 Tortoise ORM 用於 Python 異步應用",
            "評估 Redis 和 Memcached 用於高流量網站的緩存方案",
            "比較 GraphQL 和 REST API 用於移動應用後端",
            "分析 Celery 和 RQ 用於 Python 背景任務處理",
            "評估 Nginx 和 Traefik 用於微服務反向代理"
        ]
        
        selected_example = st.selectbox(
            "選擇範例問題",
            example_questions,
            key="research_example_select"
        )
        
        research_query = st.text_area(
            "編輯問題（可修改）",
            value=selected_example,
            height=100,
            help="可以修改範例問題以符合你的需求",
            key="research_example_query"
        )
    
    # 執行按鈕
    st.markdown("---")
    
    if st.button("🚀 開始技術調研", type="primary"):
        if not research_query.strip():
            st.error("❌ 請輸入研究問題")
            return
        
        # 創建進度顯示容器
        progress_container = st.empty()
        
        # 定義進度回調函數
        def update_progress(agent_name, status, total_agents, completed_agents):
            with progress_container:
                if status == "running":
                    st.progress(completed_agents / total_agents, f"🔄 {agent_name} 正在執行...")
                elif status == "completed":
                    st.progress(completed_agents / total_agents, f"✅ {agent_name} 已完成 ({completed_agents}/{total_agents})")
        
        with st.spinner("🤖 AI Agents 正在調研中... 這可能需要 5-10 分鐘"):
            try:
                # 動態導入
                from crew_modules import tech_researcher_module
                
                # 根據問題生成文件名
                import hashlib
                query_hash = hashlib.md5(research_query.encode()).hexdigest()[:8]
                output_file = f"TECH_RESEARCH_{query_hash}.md"
                
                # 執行 Crew
                result = tech_researcher_module.run_tech_researcher(
                    research_query, 
                    output_file,
                    progress_callback=update_progress
                )
                
                # 記錄到歷史（將問題存在 input_files 中）
                history_manager.add_record(
                    crew_type='research',
                    input_files=[research_query],
                    output_file=output_file,
                    success=True
                )
                
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.markdown("### ✅ 技術調研完成！")
                st.markdown(f"**研究問題**：{research_query}")
                st.markdown(f"**輸出報告**：`{output_file}`")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # 顯示結果
                if os.path.exists(output_file):
                    with open(output_file, 'r', encoding='utf-8') as f:
                        report_content = f.read()
                    
                    st.markdown("### 📊 調研報告預覽")
                    st.markdown(report_content)
                    
                    # 下載按鈕
                    st.download_button(
                        label="📥 下載報告",
                        data=report_content,
                        file_name=output_file,
                        mime="text/markdown",
                        key="download_research_report"
                    )
                
            except Exception as e:
                # 記錄錯誤到歷史
                history_manager.add_record(
                    crew_type='research',
                    input_files=[research_query],
                    output_file=output_file if 'output_file' in locals() else None,
                    success=False,
                    error_message=str(e)
                )
                
                st.error(f"❌ 執行錯誤：{str(e)}")
                st.exception(e)

# 每日技術新聞頁面
def show_daily_tech_news():
    st.markdown('<div class="main-header">📰 每日 AI 技術新聞</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">自動搜尋並分析最新 AI/ML 技術文章</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h4>🎯 功能說明</h4>
        <p>AI Agents 會自動搜尋最新的 AI/ML 技術文章，並進行深度分析：</p>
        <ul>
            <li>🔍 搜尋最新 AI 技術文章（自動排除已讀過的文章）</li>
            <li>📖 閱讀並深度分析文章內容（每篇 200-300 字摘要）</li>
            <li>📝 生成結構化的每日摘要報告</li>
            <li>⭐ 評分並推薦最值得閱讀的文章</li>
        </ul>
        <p><strong>🤖 AI Agents 團隊：</strong></p>
        <ul>
            <li>🕵️ <strong>AI News Hunter</strong> - 從多個來源搜尋最新 AI 文章</li>
            <li>📊 <strong>AI Content Analyzer</strong> - 深度閱讀並撰寫詳細摘要</li>
            <li>✍️ <strong>AI News Report Writer</strong> - 整理成易讀的每日報告</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 初始化 history manager
    from crew_modules.history_manager import history_manager
    
    # 歷史記錄區塊
    with st.expander("📚 查看歷史記錄", expanded=False):
        history = history_manager.get_history('daily_news', limit=20)
        
        if history:
            st.write(f"**總共 {len(history)} 筆記錄**")
            
            for record in history:
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    topics_str = record.get('input_files', ['未指定'])[0] if record.get('input_files') else '未指定'
                    st.write(f"🗓️ **{record.get('timestamp', 'N/A')}**")
                    st.write(f"📋 主題：{topics_str}")
                
                with col2:
                    output_file = record.get('output_file', '')
                    if output_file and os.path.exists(output_file):
                        with open(output_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        st.download_button(
                            label="📥 下載報告",
                            data=content,
                            file_name=output_file,
                            mime="text/markdown",
                            key=f"download_news_{record.get('id')}"
                        )
                
                with col3:
                    if st.button("🗑️ 刪除", key=f"delete_news_{record.get('id')}"):
                        history_manager.delete_record(record['id'])
                        st.rerun()
                
                st.markdown("---")
        else:
            st.info("📭 尚無歷史記錄")
    
    st.markdown("---")
    
    # 設定區域
    st.markdown("### ⚙️ 搜尋設定")
    
    col1, col2 = st.columns(2)
    
    with col1:
        num_articles = st.slider(
            "📊 文章數量",
            min_value=5,
            max_value=10,
            value=7,
            help="建議 5-10 篇，以確保內容質量和閱讀時間"
        )
    
    with col2:
        # 顯示已讀文章統計
        try:
            from crew_modules.daily_tech_news_module import load_read_articles
            history_data = load_read_articles()
            read_count = len(history_data.get('articles', []))
            st.metric("📚 已讀文章", f"{read_count} 篇")
        except:
            st.metric("📚 已讀文章", "0 篇")
    
    # 主題選擇
    st.markdown("### 🎯 AI 相關主題（預設已選）")
    
    st.info("💡 系統將自動搜尋 AI、Machine Learning、LLM、Generative AI 等相關主題的最新文章")
    
    # 顯示預設主題
    default_topics = [
        "Artificial Intelligence", "Machine Learning", "Deep Learning",
        "Large Language Models (LLM)", "Generative AI", "ChatGPT/GPT Models",
        "Computer Vision", "Natural Language Processing",
        "AI Agents", "Neural Networks", "Transformer Models"
    ]
    
    with st.expander("📋 查看完整搜尋主題列表", expanded=False):
        for i, topic in enumerate(default_topics, 1):
            st.write(f"{i}. {topic}")
    
    # 使用預設 AI 主題
    all_topics = default_topics
    
    # 進階選項
    with st.expander("🔧 進階選項", expanded=False):
        clear_history = st.checkbox(
            "🗑️ 清除已讀文章記錄（重新搜尋所有文章）",
            value=False,
            help="勾選後將清除已讀記錄，下次執行時會重新搜尋所有文章（可能出現重複）"
        )
        
        if clear_history and st.button("⚠️ 確認清除已讀記錄"):
            try:
                from crew_modules.daily_tech_news_module import save_read_articles
                save_read_articles({"articles": []})
                st.success("✅ 已清除已讀文章記錄")
                st.rerun()
            except Exception as e:
                st.error(f"❌ 清除失敗：{str(e)}")
    
    # 執行按鈕
    st.markdown("---")
    
    if st.button("🚀 開始搜尋 AI 技術新聞", type="primary"):
        # 創建進度顯示容器
        progress_container = st.empty()
        
        # 定義進度回調函數
        def update_progress(agent_name, status, total_agents, completed_agents):
            with progress_container:
                if status == "running":
                    st.progress(completed_agents / total_agents, f"🔄 {agent_name} 正在執行...")
                elif status == "completed":
                    st.progress(completed_agents / total_agents, f"✅ {agent_name} 已完成 ({completed_agents}/{total_agents})")
        
        with st.spinner("🤖 AI Agents 正在搜尋和分析 AI 文章... 這可能需要 2-5 分鐘"):
            try:
                # 動態導入
                from crew_modules import daily_tech_news_module
                
                # 生成輸出文件名
                today = datetime.now().strftime("%Y%m%d")
                output_file = f"TECH_NEWS_{today}.md"
                
                # 執行 Crew
                result = daily_tech_news_module.run_daily_tech_news(
                    topics=all_topics,
                    num_articles=num_articles,
                    output_file=output_file,
                    progress_callback=update_progress
                )
                
                # 記錄到歷史
                history_manager.add_record(
                    crew_type='daily_news',
                    input_files=[f"主題: {', '.join(all_topics)} ({num_articles} 篇)"],
                    output_file=output_file,
                    success=True
                )
                
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.markdown("### ✅ AI 技術新聞搜尋完成！")
                st.markdown(f"**文章數量**：{num_articles} 篇")
                st.markdown(f"**涵蓋領域**：AI、Machine Learning、LLM、Generative AI 等")
                st.markdown(f"**輸出報告**：`{output_file}`")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # 顯示結果
                if os.path.exists(output_file):
                    with open(output_file, 'r', encoding='utf-8') as f:
                        report_content = f.read()
                    
                    st.markdown("### 📊 每日 AI 新聞摘要")
                    st.markdown(report_content)  # 直接用 markdown 渲染，不會顯示 # 符號
                    
                    # 下載按鈕
                    st.download_button(
                        label="📥 下載完整報告",
                        data=report_content,
                        file_name=output_file,
                        mime="text/markdown",
                        key="download_daily_news"
                    )
                
            except Exception as e:
                # 記錄錯誤到歷史
                history_manager.add_record(
                    crew_type='daily_news',
                    input_files=[f"主題: {', '.join(all_topics)} ({num_articles} 篇)"],
                    output_file=output_file if 'output_file' in locals() else None,
                    success=False,
                    error_message=str(e)
                )
                
                st.error(f"❌ 執行錯誤：{str(e)}")
                st.exception(e)

# System Prompts 設定頁面
def show_system_prompts():
    st.markdown('<div class="main-header">💬 System Prompts 設定</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">自訂 AI Agents 的行為指示</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h4>📝 什麼是 System Prompts？</h4>
        <p>System Prompts 是給 AI Agents 的額外指示，用來控制它們的行為和輸出風格。</p>
        <p>這些設定會在每次執行時自動套用到相應的 Agent。</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 載入 prompt manager
    from crew_modules.prompt_manager import prompt_manager
    
    # 重新載入設定
    if st.button("🔄 重新載入設定"):
        prompt_manager.load_config()
        st.success("✅ 設定已重新載入")
    
    st.markdown("---")
    
    # 全域規則設定
    st.markdown("### 🌐 全域規則（所有 Agents 都會遵守）")
    
    global_rules = prompt_manager.get_global_rules()
    
    new_global_rules = st.text_area(
        "全域規則",
        value=global_rules,
        height=200,
        help="這些規則會套用到所有 AI Agents"
    )
    
    if st.button("💾 儲存全域規則"):
        prompt_manager.update_global_rules(new_global_rules)
        st.success("✅ 全域規則已儲存")
    
    st.markdown("---")
    
    # 分頁顯示各 Crew 的設定
    tab1, tab2, tab3 = st.tabs(["📖 Documentation Crew", "🔧 Refactoring Crew", "🔍 Tech Researcher"])
    
    with tab1:
        st.markdown("#### Senior Python Developer 額外指示")
        senior_dev_prompt = prompt_manager.get_agent_prompt('DOCUMENTATION_CREW', 'senior_dev_prompt')
        new_senior_dev = st.text_area(
            "Senior Developer Prompt",
            value=senior_dev_prompt,
            height=150,
            key="doc_senior_dev"
        )
        
        st.markdown("#### Technical Writer 額外指示")
        tech_writer_prompt = prompt_manager.get_agent_prompt('DOCUMENTATION_CREW', 'tech_writer_prompt')
        new_tech_writer = st.text_area(
            "Technical Writer Prompt",
            value=tech_writer_prompt,
            height=150,
            key="doc_tech_writer"
        )
        
        if st.button("💾 儲存 Documentation Crew 設定"):
            prompt_manager.update_agent_prompt('DOCUMENTATION_CREW', 'senior_dev_prompt', new_senior_dev)
            prompt_manager.update_agent_prompt('DOCUMENTATION_CREW', 'tech_writer_prompt', new_tech_writer)
            st.success("✅ Documentation Crew 設定已儲存")
    
    with tab2:
        st.markdown("#### Security Auditor 額外指示")
        security_prompt = prompt_manager.get_agent_prompt('REFACTORING_CREW', 'security_auditor_prompt')
        new_security = st.text_area(
            "Security Auditor Prompt",
            value=security_prompt,
            height=150,
            key="ref_security"
        )
        
        st.markdown("#### Clean Code Reviewer 額外指示")
        clean_code_prompt = prompt_manager.get_agent_prompt('REFACTORING_CREW', 'clean_code_reviewer_prompt')
        new_clean_code = st.text_area(
            "Clean Code Reviewer Prompt",
            value=clean_code_prompt,
            height=150,
            key="ref_clean_code"
        )
        
        st.markdown("#### Refactoring Specialist 額外指示")
        refactoring_prompt = prompt_manager.get_agent_prompt('REFACTORING_CREW', 'refactoring_specialist_prompt')
        new_refactoring = st.text_area(
            "Refactoring Specialist Prompt",
            value=refactoring_prompt,
            height=150,
            key="ref_refactoring"
        )
        
        if st.button("💾 儲存 Refactoring Crew 設定"):
            prompt_manager.update_agent_prompt('REFACTORING_CREW', 'security_auditor_prompt', new_security)
            prompt_manager.update_agent_prompt('REFACTORING_CREW', 'clean_code_reviewer_prompt', new_clean_code)
            prompt_manager.update_agent_prompt('REFACTORING_CREW', 'refactoring_specialist_prompt', new_refactoring)
            st.success("✅ Refactoring Crew 設定已儲存")
    
    with tab3:
        st.markdown("#### Research Analyst 額外指示")
        research_prompt = prompt_manager.get_agent_prompt('TECH_RESEARCHER', 'research_analyst_prompt')
        new_research = st.text_area(
            "Research Analyst Prompt",
            value=research_prompt,
            height=150,
            key="tech_research"
        )
        
        st.markdown("#### Comparison Expert 額外指示")
        comparison_prompt = prompt_manager.get_agent_prompt('TECH_RESEARCHER', 'comparison_expert_prompt')
        new_comparison = st.text_area(
            "Comparison Expert Prompt",
            value=comparison_prompt,
            height=150,
            key="tech_comparison"
        )
        
        st.markdown("#### Strategy Advisor 額外指示")
        strategy_prompt = prompt_manager.get_agent_prompt('TECH_RESEARCHER', 'strategy_advisor_prompt')
        new_strategy = st.text_area(
            "Strategy Advisor Prompt",
            value=strategy_prompt,
            height=150,
            key="tech_strategy"
        )
        
        if st.button("💾 儲存 Tech Researcher 設定"):
            prompt_manager.update_agent_prompt('TECH_RESEARCHER', 'research_analyst_prompt', new_research)
            prompt_manager.update_agent_prompt('TECH_RESEARCHER', 'comparison_expert_prompt', new_comparison)
            prompt_manager.update_agent_prompt('TECH_RESEARCHER', 'strategy_advisor_prompt', new_strategy)
            st.success("✅ Tech Researcher 設定已儲存")
    
    st.markdown("---")
    
    # 預覽功能
    with st.expander("👀 預覽增強後的 Backstory"):
        st.markdown("選擇一個 Agent 來預覽它的完整 backstory（包含全域規則和自訂規則）")
        
        crew_choice = st.selectbox(
            "選擇 Crew",
            ["Documentation Crew", "Refactoring Crew", "Tech Researcher"]
        )
        
        if crew_choice == "Documentation Crew":
            agent_choice = st.selectbox("選擇 Agent", ["Senior Developer", "Technical Writer"])
            section = 'DOCUMENTATION_CREW'
            key = 'senior_dev_prompt' if agent_choice == "Senior Developer" else 'tech_writer_prompt'
            original = "You are an expert software engineer..." if agent_choice == "Senior Developer" else "You are a skilled technical writer..."
        elif crew_choice == "Refactoring Crew":
            agent_choice = st.selectbox("選擇 Agent", ["Security Auditor", "Clean Code Reviewer", "Refactoring Specialist"])
            section = 'REFACTORING_CREW'
            key_map = {
                "Security Auditor": 'security_auditor_prompt',
                "Clean Code Reviewer": 'clean_code_reviewer_prompt',
                "Refactoring Specialist": 'refactoring_specialist_prompt'
            }
            key = key_map[agent_choice]
            original = f"You are a {agent_choice}..."
        else:
            agent_choice = st.selectbox("選擇 Agent", ["Research Analyst", "Comparison Expert", "Strategy Advisor"])
            section = 'TECH_RESEARCHER'
            key_map = {
                "Research Analyst": 'research_analyst_prompt',
                "Comparison Expert": 'comparison_expert_prompt',
                "Strategy Advisor": 'strategy_advisor_prompt'
            }
            key = key_map[agent_choice]
            original = f"You are a {agent_choice}..."
        
        enhanced = prompt_manager.get_enhanced_backstory(section, key, original)
        
        st.markdown("**完整的 Backstory：**")
        st.code(enhanced, language="text")

# 設定頁面
def show_settings():
    st.markdown('<div class="main-header">⚙️ 設定</div>', unsafe_allow_html=True)
    
    st.markdown("### 🔑 API Keys 設定")
    
    api_status = check_api_keys()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### OpenAI API Key")
        if api_status['openai']:
            st.success("✅ 已設定")
        else:
            st.error("❌ 未設定")
        
        st.markdown("""
        **如何設定：**
        1. 前往 [OpenAI Platform](https://platform.openai.com/)
        2. 建立 API Key
        3. 在專案根目錄的 `.env` 文件中設定：
        ```
        OPENAI_API_KEY=sk-your-key-here
        ```
        """)
    
    with col2:
        st.markdown("#### Serper API Key (選用)")
        if api_status['serper']:
            st.success("✅ 已設定")
        else:
            st.warning("⚠️ 未設定")
        
        st.markdown("""
        **如何設定：**
        1. 前往 [Serper.dev](https://serper.dev/)
        2. 註冊並取得 API Key（免費 2,500 次搜尋）
        3. 在 `.env` 文件中設定：
        ```
        SERPER_API_KEY=your-key-here
        ```
        """)
    
    st.markdown("---")
    
    st.markdown("### 🔄 重新載入設定")
    if st.button("重新載入環境變數"):
        from dotenv import load_dotenv
        load_dotenv(override=True)
        st.success("✅ 環境變數已重新載入")
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 📚 關於")
    st.markdown("""
    **CrewAI Code Agent** v1.0.0
    
    一個基於 CrewAI 框架的智能開發助手集合。
    
    - 🔗 [GitHub Repository](https://github.com/andynba85/CrewAI_Code_Agent)
    - 📖 [CrewAI 官方文檔](https://docs.crewai.com/)
    - 💬 有問題？歡迎開 Issue！
    """)

# 主程式
def main():
    # 🔐 要求身份驗證
    if not require_authentication():
        return
    
    # 側邊欄選單
    with st.sidebar:
        st.markdown("### 🤖 CrewAI Code Agent")
        st.markdown("---")
        
        selected = option_menu(
            menu_title=None,
            options=["首頁", "Documentation Crew", "Refactoring Crew", "Tech Researcher", "每日技術新聞", "System Prompts", "設定"],
            icons=["house", "book", "tools", "search", "newspaper", "chat-dots", "gear"],
            menu_icon="cast",
            default_index=0,
        )
        
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666; font-size: 0.8rem;'>
            Made with ❤️ using CrewAI<br>
            © 2025 Andy Hsieh
        </div>
        """, unsafe_allow_html=True)
        
        # 顯示用戶資訊和登出按鈕（放在最底部）
        show_user_info()

    
    # 根據選擇顯示對應頁面
    if selected == "首頁":
        show_home()
    elif selected == "Documentation Crew":
        show_documentation_crew()
    elif selected == "Refactoring Crew":
        show_refactoring_crew()
    elif selected == "Tech Researcher":
        show_tech_researcher()
    elif selected == "每日技術新聞":
        show_daily_tech_news()
    elif selected == "System Prompts":
        show_system_prompts()
    elif selected == "設定":
        show_settings()

if __name__ == "__main__":
    main()
