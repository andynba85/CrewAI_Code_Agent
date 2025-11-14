# 🤖 CrewAI Code Agent - AI 驅動的開發助手

一個基於 CrewAI 框架的智能開發助手集合，專門為軟件工程師打造。透過角色扮演（Role-Playing）與任務編排（Task Orchestration），自動化處理文檔生成、代碼審查、技術調研等繁瑣任務。

## 📋 專案概述

本專案包含三個不同複雜度的 CrewAI 應用，涵蓋開發者日常工作中最痛苦的環節：

1. **🔰 初級應用**：自動化文檔生成小隊 (Documentation Crew)
2. **🔧 中級應用**：智慧 Code Review 與重構建議 (Refactoring Crew)  
3. **🔍 進階應用**：技術調研與決策助手 (Tech Stack Researcher)

## ✨ 核心特色

- **🎭 多角色協作**：模擬真實團隊中的不同角色（開發者、技術寫手、資安專家、架構師等）
- **🔄 任務編排**：智能的任務依賴與執行順序管理
- **🌐 聯網搜尋**：整合最新的網路資訊進行技術調研
- **📊 結構化輸出**：自動生成格式完美的 Markdown 報告
- **🛡️ 安全審查**：自動識別常見的安全漏洞和代碼問題

## 🚀 快速開始

### 🌐 使用 Web UI (推薦)

最簡單的方式是使用我們的 Streamlit Web 介面：

```powershell
# 1. 啟動虛擬環境
.\CrewAI_Code_Agent_venv\Scripts\Activate.ps1

# 2. 確保已安裝依賴
pip install -r requirements.txt

# 3. 設定 API Key（編輯 .env 文件）
# OPENAI_API_KEY=your_key_here

# 4. 啟動 Web UI
streamlit run app.py
```

Web UI 會自動在瀏覽器開啟 `http://localhost:8501`

### 💻 或使用命令列

### 環境需求

- Python 3.8+
- OpenAI API Key
- Serper API Key (選用，用於網路搜尋)

### 安裝步驟

1. **克隆專案**
```bash
git clone https://github.com/yourusername/CrewAI_Code_Agent.git
cd CrewAI_Code_Agent
```

2. **建立虛擬環境**
```bash
python -m venv CrewAI_Code_Agent_venv

# Windows
.\CrewAI_Code_Agent_venv\Scripts\Activate.ps1

# macOS/Linux
source CrewAI_Code_Agent_venv/bin/activate
```

3. **安裝依賴**
```bash
pip install -r requirements.txt
```

4. **設定環境變數**
```bash
# 複製環境變數範本
cp .env.example .env

# 編輯 .env 並填入你的 API Keys
# OPENAI_API_KEY=your_openai_key_here
# SERPER_API_KEY=your_serper_key_here (optional)
```

## 📚 應用說明

### 1️⃣ Documentation Crew - 自動化文檔生成

**痛點**：寫完代碼後懶得寫 README 或 API 文件

**解決方案**：自動閱讀代碼並生成完整的技術文檔

**使用方式**：
```bash
python 1_documentation_crew.py
```

**Agents 角色**：
- 📖 **Code Interpreter** (Senior Python Developer)：深度分析代碼邏輯與架構
- ✍️ **Technical Writer**：將技術分析轉化為易讀的文檔

**輸出範例**：
- 專案概述
- 安裝指南
- 使用範例
- API 參考
- 架構說明

---

### 2️⃣ Refactoring Crew - 智慧 Code Review

**痛點**：自己寫的代碼可能有優化空間，但不知從何改起

**解決方案**：全方位代碼審查，包含安全性、代碼品質、重構建議

**使用方式**：
```bash
python 2_refactoring_crew.py
```

**Agents 角色**：
- 🛡️ **Security Auditor**：掃描 OWASP Top 10 安全漏洞
  - SQL Injection
  - Hardcoded Secrets
  - Command Injection
  - 弱加密算法
  - 不安全的反序列化
  
- 🧹 **Clean Code Reviewer**：檢查代碼品質
  - SOLID 原則
  - 命名規範
  - 函數複雜度
  - 代碼重複（DRY）
  - 設計模式應用
  
- 🔧 **Refactoring Specialist**：提供重構版本
  - 綜合前兩者建議
  - 生成優化後的代碼
  - Before/After 比較

**輸出範例**：
- 問題清單（Critical/High/Medium/Low）
- 重構後的代碼
- 改進說明
- 測試建議

---

### 3️⃣ Tech Stack Researcher - 技術選型助手

**痛點**：新專案要選型（Next.js vs Remix？PostgreSQL vs MongoDB？）需要大量調研

**解決方案**：自動搜尋最新資訊，進行優劣勢分析，給出決策建議

**使用方式**：
```bash
python 3_tech_researcher_crew.py
```

**Agents 角色**：
- 🔍 **Research Analyst**：搜尋最新技術資訊
  - 官方文檔
  - GitHub Stars & Activity
  - 效能基準測試
  - 社群討論
  
- ⚖️ **Comparison Expert**：建立比較矩陣
  - 功能對比表
  - 性能比較
  - 生態系統成熟度
  - Pros & Cons
  
- 🎯 **Strategy Advisor** (CTO)：給出最終建議
  - 基於專案需求
  - 考量團隊能力
  - 長期維護性
  - 實施路線圖

**輸出範例**：
- 研究摘要
- 詳細比較表
- 推薦方案（含信心度）
- 實施路線圖
- 風險評估

## 💡 使用範例

### 🌐 使用 Web UI (最簡單)

1. 啟動 Web UI：`streamlit run app.py`
2. 在瀏覽器中選擇功能
3. 上傳文件或輸入問題
4. 點擊按鈕開始執行
5. 在頁面上查看結果並下載報告

### 💻 使用命令列

### 範例 1：為舊專案生成文檔

```bash
# 準備一個 Python 文件
cp example_code.py my_project.py

# 執行文檔生成
python 1_documentation_crew.py
# 輸入: my_project.py
# 輸出: DOCS_my_project.md
```

### 範例 2：審查並優化代碼

```bash
# 準備要審查的代碼
python 2_refactoring_crew.py
# 輸入: example_code.py
# 輸出: REFACTORING_example_code.md
```

### 範例 3：技術選型調研

```bash
python 3_tech_researcher_crew.py
# 輸入: "比較 FastAPI 和 Django Channels 用於高併發的即時聊天應用"
# 輸出: TECH_RESEARCH_REPORT.md
```

## 🎨 自訂與擴展

### 調整 Agent 行為

你可以修改每個 Agent 的 `backstory` 和 `goal` 來客製化其行為：

```python
senior_dev = Agent(
    role='Senior Python Developer',
    goal='你的自訂目標',
    backstory='你的自訂背景故事',
    tools=[your_tools],
    verbose=True
)
```

### 添加自訂工具

CrewAI 支援多種工具，你可以根據需求添加：

```python
from crewai_tools import (
    FileReadTool,
    DirectoryReadTool,
    SerperDevTool,
    ScrapeWebsiteTool,
    # ... 更多工具
)
```

### 修改執行流程

支援兩種流程模式：

```python
# 循序執行
process=Process.sequential

# 階層式（需要 Manager Agent）
process=Process.hierarchical
```

## 📦 專案結構

```
CrewAI_Code_Agent/
├── app.py                       # 🌐 Streamlit Web UI 主程式
├── crew_modules/                # 📦 可重用的 Crew 模組
│   ├── __init__.py
│   ├── documentation_crew_module.py
│   ├── refactoring_crew_module.py
│   └── tech_researcher_module.py
├── 1_documentation_crew.py      # 文檔生成應用（命令列版）
├── 2_refactoring_crew.py        # Code Review 應用（命令列版）
├── 3_tech_researcher_crew.py    # 技術調研應用（命令列版）
├── example_code.py              # 測試用範例代碼（有問題）
├── example_fastapi.py           # 測試用範例代碼（乾淨）
├── requirements.txt             # Python 依賴
├── .env.example                 # 環境變數範本
├── .gitignore                   # Git 忽略文件
└── README.md                    # 專案說明（本文件）
```

## ⚙️ 設定說明

### OpenAI API Key

**必需**。用於驅動 LLM Agent。

1. 前往 [OpenAI Platform](https://platform.openai.com/)
2. 建立 API Key
3. 在 `.env` 中設定：
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```

### Serper API Key

**選用**。僅用於 Tech Researcher（需要網路搜尋）。

1. 前往 [Serper.dev](https://serper.dev/)
2. 註冊並取得 API Key（免費方案有 2,500 次搜尋額度）
3. 在 `.env` 中設定：
   ```
   SERPER_API_KEY=your-serper-key-here
   ```

如果不設定，Tech Researcher 仍可運作，但會依賴 LLM 的既有知識（可能不是最新資訊）。

## 🔧 進階設定

### 更換 LLM 模型

預設使用 `gpt-4-turbo-preview`，你可以修改為其他模型：

```python
# 在 .env 中
OPENAI_MODEL_NAME=gpt-4
# 或
OPENAI_MODEL_NAME=gpt-3.5-turbo
```

### 調整 Agent Verbose 等級

```python
agent = Agent(
    # ...
    verbose=True,  # 顯示詳細執行過程
    # 或
    verbose=False  # 僅顯示結果
)
```

## 🤝 貢獻

歡迎貢獻！如果你有新的 Agent 想法或改進建議：

1. Fork 本專案
2. 建立新分支 (`git checkout -b feature/AmazingFeature`)
3. 提交修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 📝 授權

本專案採用 MIT 授權條款。

## 🙏 致謝

- [CrewAI](https://github.com/joaomdmoura/crewAI) - 強大的 Multi-Agent 框架
- [OpenAI](https://openai.com/) - GPT 語言模型
- [Serper](https://serper.dev/) - Google 搜尋 API

## 📮 聯絡方式

如有問題或建議，歡迎開 Issue 或聯繫：

- GitHub: [@andynba85](https://github.com/andynba85)
- Email: your.email@example.com

## 🎯 下一步計畫

- [ ] 添加更多 Agent 範例（測試生成、API 文檔、Git Commit 訊息）
- [ ] 支援更多 LLM 提供商（Anthropic Claude, Google Gemini）
- [ ] 建立 Web UI 介面
- [ ] 加入 Memory 功能（讓 Agent 記住歷史對話）
- [ ] 支援團隊協作（多人共用知識庫）

---

⭐ 如果這個專案對你有幫助，請給個 Star！