# 🚀 CrewAI Code Agent - Web UI 完整設定指南

## ✅ 已完成的設定

你的虛擬環境 `CrewAI_Code_Agent_venv` 已經建立並啟動。

## 📦 接下來的步驟

### 1️⃣ 安裝 Web UI 依賴

```powershell
# 確保虛擬環境已啟動（應該看到 (CrewAI_Code_Agent_venv) 前綴）
pip install streamlit streamlit-option-menu
```

### 2️⃣ 設定 API Key

1. **複製環境變數範本**：
```powershell
Copy-Item .env.example .env
```

2. **編輯 .env 文件**（使用記事本或 VS Code）：
```
OPENAI_API_KEY=sk-your-actual-key-here
OPENAI_MODEL_NAME=gpt-4-turbo-preview
SERPER_API_KEY=your_serper_key_here  # 選用
OUTPUT_DIR=./output
```

### 3️⃣ 啟動 Web UI

#### 方式 A：使用啟動腳本（推薦）
```powershell
.\start_ui.ps1
```

#### 方式 B：手動啟動
```powershell
streamlit run app.py
```

### 4️⃣ 開始使用

瀏覽器會自動開啟 `http://localhost:8501`

如果沒有自動開啟，請手動在瀏覽器輸入該網址。

---

## 🎯 快速測試

### 測試 1：Documentation Crew

1. 在 Web UI 選擇「Documentation Crew」
2. 文件路徑輸入：`example_code.py`
3. 點擊「🚀 開始生成文檔」
4. 等待 3-5 分鐘
5. 查看並下載生成的文檔

### 測試 2：Refactoring Crew

1. 選擇「Refactoring Crew」
2. 文件路徑輸入：`example_code.py`（這個文件故意包含安全問題）
3. 點擊「🔍 開始 Code Review」
4. 等待 5-10 分鐘
5. 查看發現的問題和重構建議

### 測試 3：Tech Researcher

1. 選擇「Tech Researcher」
2. 輸入問題：`比較 FastAPI 和 Flask 用於 RESTful API 開發`
3. 點擊「🚀 開始技術調研」
4. 等待 5-10 分鐘
5. 查看調研報告和建議

---

## 📁 專案檔案說明

### Web UI 相關檔案

- **app.py**：Streamlit Web UI 主程式
  - 包含首頁、三個功能頁面、設定頁面
  - 友善的圖形化介面
  - 支援文件上傳和下載

- **crew_modules/**：可重用的模組
  - `documentation_crew_module.py`：文檔生成邏輯
  - `refactoring_crew_module.py`：代碼審查邏輯
  - `tech_researcher_module.py`：技術調研邏輯

- **start_ui.ps1**：Windows PowerShell 快速啟動腳本
  - 自動檢查環境
  - 自動啟動虛擬環境
  - 啟動 Streamlit

### 命令列版本（舊版，仍可使用）

- `1_documentation_crew.py`
- `2_refactoring_crew.py`
- `3_tech_researcher_crew.py`

### 測試文件

- **example_code.py**：包含多種問題的範例代碼
  - 硬編碼密鑰
  - SQL Injection 風險
  - 使用弱加密（MD5）
  - 不安全的 pickle
  - 命名不佳
  - 缺乏錯誤處理

- **example_fastapi.py**：乾淨的 FastAPI 範例
  - 遵循最佳實踐
  - 完整的類型提示
  - 良好的文檔字串
  - 適當的錯誤處理

---

## 🌟 Web UI 特色

### ✨ 視覺化介面
- 🎨 現代化設計
- 📱 響應式佈局
- 🎯 清晰的導航

### 🚀 易用性
- 📤 支援文件上傳
- 📥 一鍵下載報告
- 👀 即時預覽結果
- ⚙️ API Key 狀態檢查

### 🛡️ 安全性
- 🔐 環境變數管理
- ✅ 輸入驗證
- 📝 詳細的錯誤訊息

### 📊 功能完整
- 📖 Documentation Crew
- 🔧 Refactoring Crew
- 🔍 Tech Researcher
- ⚙️ 設定管理

---

## 💡 使用建議

### 第一次使用

1. **先測試 Documentation Crew**
   - 使用 `example_fastapi.py`（乾淨的代碼）
   - 看看 AI 如何分析良好的代碼

2. **再測試 Refactoring Crew**
   - 使用 `example_code.py`（有問題的代碼）
   - 看看 AI 如何發現問題並給出建議

3. **最後測試 Tech Researcher**
   - 用實際的技術選型問題
   - 比較你正在考慮的技術

### 實際專案使用

1. **文檔生成**
   - 為你的專案主文件生成 README
   - 為複雜的模組生成說明

2. **代碼審查**
   - 在提交 PR 前先自我審查
   - 學習安全最佳實踐
   - 發現潛在的技術債

3. **技術決策**
   - 新專案技術選型
   - 現有系統升級評估
   - 工具/框架比較

---

## 🐛 故障排除

### 問題 1：啟動時出現 "streamlit: command not found"
```powershell
# 解決方法：確保虛擬環境已啟動
.\CrewAI_Code_Agent_venv\Scripts\Activate.ps1

# 重新安裝
pip install streamlit streamlit-option-menu
```

### 問題 2：瀏覽器沒有自動開啟
手動開啟瀏覽器並前往：`http://localhost:8501`

### 問題 3：顯示 "OpenAI API Key 未設定"
1. 檢查 `.env` 文件是否存在
2. 確認 `OPENAI_API_KEY` 設定正確
3. 在 Web UI 設定頁面點擊「重新載入環境變數」

### 問題 4：執行很慢或超時
- 這是正常的！AI Agents 需要時間思考
- Documentation Crew：約 3-5 分鐘
- Refactoring Crew：約 5-10 分鐘（3 個 Agents）
- Tech Researcher：約 5-10 分鐘

### 問題 5：顯示 Import Error
```powershell
# 重新安裝所有依賴
pip install -r requirements.txt
```

---

## 📊 系統需求

### 最低配置
- Python 3.8+
- 4GB RAM
- 穩定的網路連線（用於 API 調用）

### 推薦配置
- Python 3.10+
- 8GB+ RAM
- 高速網路連線

### API 配額
- OpenAI API：需要有額度的 API Key
- Serper API：免費方案 2,500 次搜尋/月（選用）

---

## 🎓 進階使用

### 客製化 Agents

編輯 `crew_modules/` 下的模組文件，修改 Agent 的 `backstory` 和 `goal`。

### 添加新功能

1. 在 `crew_modules/` 建立新模組
2. 在 `app.py` 添加新頁面函數
3. 在側邊欄選單加入新選項

### 調整 UI 樣式

編輯 `app.py` 中的 CSS 部分來自訂顏色和樣式。

---

## 📞 需要協助？

- 📖 閱讀 `WEB_UI_GUIDE.md` 獲取詳細使用指南
- 📝 查看 `README.md` 了解專案架構
- 🐛 在 GitHub 開 Issue 回報問題
- 💬 查看終端機的詳細錯誤訊息

---

## 🎉 開始使用

現在你已經完成所有設定！執行以下命令開始：

```powershell
.\start_ui.ps1
```

或

```powershell
streamlit run app.py
```

祝你使用愉快！🚀
