# CrewAI Code Agent - Web UI 使用指南

## 🌐 啟動 Web UI

### Windows PowerShell
```powershell
# 方式 1：使用啟動腳本（推薦）
.\start_ui.ps1

# 方式 2：手動啟動
.\CrewAI_Code_Agent_venv\Scripts\Activate.ps1
streamlit run app.py
```

### macOS/Linux
```bash
# 啟動虛擬環境
source CrewAI_Code_Agent_venv/bin/activate

# 啟動 Web UI
streamlit run app.py
```

## 📱 Web UI 功能介紹

### 首頁
- 檢查 API Keys 設定狀態
- 查看三大功能介紹
- 快速開始指南

### Documentation Crew 頁面
1. **輸入代碼文件路徑** 或 **上傳文件**
2. 點擊 "🚀 開始生成文檔"
3. 等待 AI Agents 完成分析（約 3-5 分鐘）
4. 在頁面上預覽生成的文檔
5. 點擊 "📥 下載文檔" 保存

### Refactoring Crew 頁面
1. **輸入要審查的代碼文件路徑** 或 **上傳文件**
2. 點擊 "🔍 開始 Code Review"
3. 等待 AI Agents 完成審查（約 5-10 分鐘）
4. 查看審查報告：
   - 🚨 Critical Issues（必須修復）
   - ⚠️ Important Improvements（應該修復）
   - 💡 Nice-to-Have（可選修復）
   - ✨ Refactored Code（優化後的代碼）
5. 下載完整報告

### Tech Researcher 頁面
1. **輸入技術調研問題**（可參考範例問題）
2. 點擊 "🚀 開始技術調研"
3. 等待 AI Agents 完成調研（約 5-10 分鐘）
   - 如果有設定 Serper API Key，會搜尋最新資訊
   - 如果沒有，會使用 LLM 既有知識
4. 查看調研報告：
   - 📊 Research Findings（調研結果）
   - ⚖️ Comparison（比較分析）
   - 🏆 Recommendation（推薦建議）
   - 🚀 Implementation Roadmap（實施路線圖）
5. 下載報告

### 設定頁面
- 查看 API Keys 設定狀態
- 查看設定指南
- 重新載入環境變數
- 查看專案資訊

## 💡 使用技巧

### 1. 文件上傳
- 支援直接上傳 Python 文件（.py）
- 上傳後會自動保存為臨時文件
- 適合快速測試小文件

### 2. 文件路徑
- 可以使用相對路徑（相對於專案根目錄）
- 也可以使用絕對路徑
- 範例：
  - `example_code.py`
  - `./examples/test.py`
  - `C:\Users\...\myproject\main.py`

### 3. 執行時間
- Documentation Crew：約 3-5 分鐘
- Refactoring Crew：約 5-10 分鐘（因為有 3 個 Agents）
- Tech Researcher：約 5-10 分鐘（取決於是否使用網路搜尋）

### 4. 結果保存
- 所有報告都會保存在專案根目錄
- 文檔：`DOCS_<filename>.md`
- 重構報告：`REFACTORING_<filename>.md`
- 調研報告：`TECH_RESEARCH_REPORT.md`

## 🎨 自訂 UI

### 修改主題顏色
編輯 `app.py` 中的 CSS 部分：
```python
st.markdown("""
<style>
    .main-header {
        color: #1E88E5;  /* 改成你喜歡的顏色 */
    }
</style>
""", unsafe_allow_html=True)
```

### 添加新功能
1. 在 `crew_modules/` 建立新的模組
2. 在 `app.py` 新增頁面函數
3. 在側邊欄選單加入選項

## 🐛 常見問題

### Q1: 啟動後瀏覽器沒有自動開啟
手動開啟瀏覽器並前往：`http://localhost:8501`

### Q2: 顯示 "Module not found" 錯誤
確保已安裝所有依賴：
```powershell
pip install -r requirements.txt
```

### Q3: 執行中途出現錯誤
- 檢查 API Key 是否正確設定
- 檢查網路連線
- 查看終端機的詳細錯誤訊息

### Q4: 想停止正在執行的任務
目前不支援中途停止，請等待執行完成或直接關閉瀏覽器頁面

### Q5: 如何更新 .env 設定
1. 編輯 `.env` 文件
2. 在 Web UI 的「設定」頁面點擊「重新載入環境變數」
3. 或重新啟動 Streamlit

## 📊 效能優化

### 如果執行太慢：
1. 使用更快的 LLM 模型（如 `gpt-3.5-turbo`）
2. 在模組代碼中設定 `verbose=False`
3. 使用較小的代碼文件進行測試

### 如果想要更詳細的輸出：
1. 在終端機查看完整的執行日誌
2. 模組代碼中保持 `verbose=True`

## 🎯 最佳實踐

1. **第一次使用**：先用 `example_code.py` 測試
2. **大型專案**：先測試單個文件，確認可行後再分析整個專案
3. **技術調研**：問題描述要清楚具體，包含使用場景
4. **API 使用**：注意 OpenAI API 的費用，合理使用

## 📞 需要幫助？

- 查看終端機的詳細日誌
- 閱讀 `README.md` 獲取更多資訊
- 在 GitHub 開 Issue 回報問題

---

祝你使用愉快！🚀
