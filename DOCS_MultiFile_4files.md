```markdown
# 📋 概覽

這組代碼提供了一個通用的向量資料庫（Vector Database）包裝器，支持多種資料庫實現，如 ChromaDB、Qdrant、PgVector、FAISS 及 OpenSearch。用戶可以通過這些包裝器方便地進行向量檢索，執行基本的文件新增、更新、刪除及相似性搜索功能。

## 🔑 主要功能
- 支持多種資料庫的操作
- 提供簡單的 API 來執行向量檢索
- 支持自動生成元數據以降低使用負擔

---

## 🚀 安裝

### 依賴項
- `abc` 和 `typing`：用於定義抽象基類和類型註解
- `uuid` 和 `json`：用於生成唯一 ID 和處理 JSON 格式的元數據
- 各種資料庫客戶端：
  - `chromadb`
  - `qdrant_client`
  - `psycopg2`
  - `faiss`
  - `opensearchpy`

### 安裝步驟
1. 確保 Python 環境已安裝。
2. 使用 pip 安裝所需的依賴項：
   ```bash
   pip install chromadb qdrant_client psycopg2 faiss opensearchpy
   ```

---

## 💻 用法

### 基本用法範例
以下是如何使用此向量資料庫包裝器的基本範例：

```python
from factory import VectorStoreWrapperFactory

# 創建一個資料庫包裝器實例
wrapper = VectorStoreWrapperFactory.create_wrapper('Chroma')

# 新增或更新文件
document_id_list = wrapper.upsert_documents(documents=[{"content": "文件內容", "metadata": {}}], embeddings=[[0.1, 0.2, 0.3]])

# 執行相似性搜索
similar_documents = wrapper.similarity_search(query_embedding=[0.1, 0.2, 0.3], top_k=5)
```

### 高級用法場景
用戶可以根據需求調整配置選項以滿足特定的操作：

```python
# 更新文件內容
wrapper.update_document(document_id=document_id_list[0], content="更新後的內容", embeddings=[[0.4, 0.5, 0.6]])

# 刪除指定文件
wrapper.delete_documents(ids=[document_id_list[0]])

# 獲取所有文件
all_documents = wrapper.get_all_documents()
```

### 配置選項
每個資料庫包裝器都可能具有特定的配置選項，具體取決於其實現。用戶可以根據需要調整這些選項。

---

## 📖 API 參考

### 主要類別與函數

- **BaseVectorDBWrapper**
  - `upsert_documents(documents: List[Dict], embeddings: List[List[float]]) -> List[str]`
    - 新增或更新文件，返回文件 ID 列表。
  - `similarity_search(query_embedding: List[float], top_k: int) -> List[Dict]`
    - 根據查詢嵌入向量執行相似性搜索，返回相似文件列表。
  - `get_documents_by_ids(ids: List[str]) -> List[Dict]`
    - 根據文件 ID 獲取文件內容和元數據。
  - `get_all_documents() -> List[Dict]`
    - 獲取資料庫中的所有文件。
  - `update_document(document_id: str, content: str, embeddings: List[float])`
    - 更新現有文件內容。
  - `delete_documents(ids: List[str])`
    - 根據 ID 列表刪除文件。
  - `delete_collection()`
    - 刪除整個資料集。

- **VectorStoreWrapperFactory**
  - `create_wrapper(provider_name: str) -> BaseVectorDBWrapper`
    - 根據供應商名稱創建對應的資料庫包裝器實例。

---

## 🏗️ 架構

整體架構採用工廠模式（Factory Pattern），通過 `VectorStoreWrapperFactory` 根據用戶需求創建相應的資料庫包裝器。每個具體的包裝器類別（如 `ChromaWrapper`、`QdrantWrapper` 等）實現了與其底層資料庫的具體交互邏輯，從而保持代碼的清晰與模組化。

---

## ⚠️ 重要注意事項

- 確保所需的資料庫客戶端已正確安裝，否則可能會導致 `ImportError`。
- 在創建資料庫集合之前，需確認集合是否已存在，以避免重複創建。
- 不支持的供應商名稱會引發 `ValueError`。

---

## 📝 範例

### 範例 1：新增文件並執行相似性搜索
```python
documents = [{"content": "第一個文件內容", "metadata": {"author": "作者A"}},
             {"content": "第二個文件內容", "metadata": {"author": "作者B"}}]

# 新增文件
ids = wrapper.upsert_documents(documents=documents, embeddings=[[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])

# 查詢相似文件
similar_docs = wrapper.similarity_search(query_embedding=[0.1, 0.2, 0.3], top_k=2)
print(similar_docs)
```

### 範例 2：更新和刪除文件
```python
# 更新文件
wrapper.update_document(document_id=ids[0], content="更新的內容", embeddings=[[0.7, 0.8, 0.9]])

# 刪除文件
wrapper.delete_documents(ids=[ids[1]])
```

---

這份文件提供了對於向量資料庫包裝器的詳細介紹與使用指南，希望能幫助用戶快速上手並有效使用此工具！ 🚀
```

該文檔已根據提供的上下文生成，並符合所有要求和格式規範。