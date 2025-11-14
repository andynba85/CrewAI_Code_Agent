# 快速啟動指南

## 🎯 快速測試三個應用

### 1. 設定環境

```powershell
# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境
.\venv\Scripts\activate

# 安裝依賴
pip install -r requirements.txt

# 設定 API Key
# 將 .env.example 複製為 .env，並填入你的 OpenAI API Key
cp .env.example .env
```

### 2. 測試文檔生成 (5 分鐘)

```powershell
# 執行文檔生成器
python 1_documentation_crew.py

# 當提示輸入時，按 Enter 使用預設的 example_code.py
# 或輸入你自己的 Python 文件路徑

# 執行完成後會生成：DOCS_example_code.md
```

### 3. 測試 Code Review (5-10 分鐘)

```powershell
# 執行 Code Review
python 2_refactoring_crew.py

# 當提示輸入時，按 Enter 使用預設的 example_code.py
# 這個範例代碼故意包含安全問題和品質問題

# 執行完成後會生成：REFACTORING_example_code.md
```

### 4. 測試技術調研 (5-10 分鐘)

```powershell
# 執行技術調研
python 3_tech_researcher_crew.py

# 輸入你的技術問題，例如：
# "比較 FastAPI 和 Django Channels 用於高併發的即時聊天應用"

# 注意：此功能需要 SERPER_API_KEY，如果沒有，Agent 會使用既有知識
# 執行完成後會生成：TECH_RESEARCH_REPORT.md
```

## 💡 使用建議

### Documentation Crew 適合用於：
- ✅ 為舊專案補文檔
- ✅ 自動生成 API 文檔
- ✅ 理解別人寫的複雜代碼
- ✅ 快速建立專案 README

### Refactoring Crew 適合用於：
- ✅ Code Review 自動化
- ✅ 發現安全漏洞
- ✅ 學習最佳實踐
- ✅ Legacy Code 重構規劃

### Tech Researcher 適合用於：
- ✅ 新專案技術選型
- ✅ 學習新技術時的比較研究
- ✅ 評估升級方案（例如：Python 2 → 3）
- ✅ 尋找最佳工具/框架

## 🎨 自訂範例

### 範例 1：為你的專案生成文檔

```powershell
python 1_documentation_crew.py
# 輸入：path/to/your/project/main.py
```

### 範例 2：審查你的代碼

```powershell
python 2_refactoring_crew.py
# 輸入：path/to/your/code.py
```

### 範例 3：技術調研問題範例

```
- "比較 Next.js 和 Remix 用於建立 SEO 友好的電商網站"
- "評估 PostgreSQL vs MongoDB 用於社交媒體應用"
- "分析 React 和 Vue.js 用於企業後台管理系統"
- "比較 Docker 和 Kubernetes 用於微服務部署"
```

## ⚡ 效能優化

如果執行太慢，可以：

1. **使用更快的模型**：在 `.env` 中改用 `gpt-3.5-turbo`
2. **減少 verbose 輸出**：在代碼中將 `verbose=True` 改為 `False`
3. **限制任務範圍**：修改 Task description，讓分析更聚焦

## 🐛 常見問題

### Q1: Import Error - 找不到 crewai

```powershell
pip install crewai crewai-tools
```

### Q2: OpenAI API Key 錯誤

確認 `.env` 文件中的 `OPENAI_API_KEY` 設定正確

### Q3: 執行很慢

這是正常的！因為 Agent 需要思考和多次調用 LLM。
通常一個完整的 Crew 執行需要 3-10 分鐘。

### Q4: Serper API Key 在哪裡取得？

1. 前往 https://serper.dev
2. 註冊帳號（Google 登入即可）
3. 免費方案有 2,500 次搜尋額度
4. 複製 API Key 到 `.env`

## 🎓 學習建議

1. **先跑一遍範例**：理解每個 Crew 的輸出
2. **閱讀生成的報告**：看看 Agent 怎麼思考和分析
3. **修改 Agent backstory**：調整 Agent 的行為和風格
4. **嘗試不同的代碼**：用你自己的專案測試
5. **客製化 Task**：根據你的需求修改任務描述

## 📚 延伸閱讀

- [CrewAI 官方文檔](https://docs.crewai.com/)
- [CrewAI GitHub](https://github.com/joaomdmoura/crewAI)
- [OpenAI API 文檔](https://platform.openai.com/docs)

---

祝你玩得開心！如有問題歡迎開 Issue 討論。
