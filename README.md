# 🧳 旅遊產品比對系統

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red.svg)](https://streamlit.io/)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Run-4285F4.svg)](https://cloud.google.com/run)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> 一個基於 Streamlit 的智慧旅遊產品比對網頁應用程式，使用 Jaccard 相似度算法自動比較兩個供應商的產品，並提供詳細的分析報告。

## 🌟 線上體驗

**🔗 線上服務**: [https://travel-product-matching-90644723399.asia-east1.run.app](https://travel-product-matching-90644723399.asia-east1.run.app)

**🔑 存取密碼**: 請聯絡專案維護者取得存取密碼

> 系統部署於 Google Cloud Run，提供 24/7 穩定服務

## ✨ 核心功能

### 📊 智慧比對引擎
- **Jaccard 相似度算法**: 精確計算產品名稱相似度
- **中英文智慧翻譯**: 自動處理多語言產品名稱
- **國家維度比對**: 按產品所屬國家進行精準比對
- **可調參數設定**: 相似度門檻、詞彙差異限制等

### 🔒 安全機制
- **密碼保護**: 企業級存取控制
- **Session 管理**: 24小時有效期，自動過期保護
- **使用統計**: 即時追蹤使用次數和狀態

### 📁 檔案處理
- **多格式支援**: CSV、Excel (.xlsx/.xls)
- **多編碼相容**: UTF-8、Big5、GBK 自動偵測
- **資料驗證**: 必要欄位檢查和品質驗證
- **即時預覽**: 上傳後立即顯示前 10 筆資料

### 📈 分析與視覺化
- **統計摘要**: 總比對數、平均相似度、價格差異分析
- **圖表展示**: 相似度分布圓餅圖、價格差異直方圖、散點圖
- **國家統計**: 按國家分組的詳細統計報告
- **排行榜**: 相似度最高的產品清單

### 💾 結果匯出
- **CSV 格式**: 標準格式，易於後續處理
- **Excel 格式**: 含格式化的專業報告
- **時間戳記**: 自動加入匯出時間標記

## 🚀 快速開始

### 方式一：本機部署

#### 1️⃣ 環境準備
```bash
# 確保 Python 3.8+ 已安裝
python --version

# 複製專案
git clone <repository-url>
cd travel_product_matching_public
```

#### 2️⃣ 依賴安裝
```bash
# 使用 pip
pip install -r requirements.txt

# 或使用 Pipenv (推薦)
pip install pipenv
pipenv install
```

#### 3️⃣ 啟動應用程式
```bash
# 標準啟動
streamlit run app.py

# 使用 Pipenv
pipenv run streamlit run app.py --server.port 9001

# Windows 一鍵啟動
start.bat
```

#### 4️⃣ 存取應用程式
開啟瀏覽器訪問：`http://localhost:8501`

> 📋 **環境變數設定**: 詳細的環境變數配置說明請參考 [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md)

### 方式二：Docker 部署

```bash
# 建立容器映像
docker build -t travel-product-matching .

# 執行容器
docker run -p 8080:8080 -e APP_PASSWORD=your_secure_password travel-product-matching
```

### 方式三：Google Cloud Run 部署

```bash
# 使用 gcloud CLI 部署
gcloud run deploy travel-product-matching \
  --source . \
  --region=asia-east1 \
  --set-env-vars=APP_PASSWORD=your_secure_password \
  --allow-unauthenticated
```

## 📁 專案結構

```
travel_product_matching_public/
├── 🔹 核心應用程式
│   ├── app.py                    # 本機版主程式
│   ├── main_gcp.py              # GCP 雲端版 (含密碼保護)
│   └── src/
│       ├── __init__.py
│       ├── file_handler.py      # 檔案上傳與處理
│       ├── matcher.py           # Jaccard 比對核心
│       ├── translator.py        # 翻譯服務模組
│       └── utils.py            # 工具函數與視覺化
│
├── 🔹 部署配置
│   ├── Dockerfile               # 容器化配置
│   ├── requirements.txt         # 本機依賴
│   ├── requirements-gcp.txt     # 雲端精簡依賴
│   ├── Pipfile                 # Pipenv 配置
│   ├── deploy-gcp.sh           # GCP 部署腳本
│   └── .streamlit/
│       └── config.toml         # Streamlit 配置
│
├── 🔹 啟動腳本
│   └── start.bat               # Windows 啟動腳本
│
├── 🔹 文件資料
│   ├── README.md               # 專案說明 (本文件)
│   ├── STARTUP_GUIDE.md        # 快速啟動指南
│   ├── GCP_deployment_guide.md # GCP 部署詳細指南
│   ├── business_todo.md        # 商業功能待辦事項
│   └── .github/
│       └── copilot-instructions.md # Copilot 開發指引
│
└── 🔹 範例資料
    └── data/                   # 測試用範例檔案
```

## 📋 檔案格式要求

### 必要欄位
系統要求輸入檔案包含以下欄位：

| 欄位名稱 | 說明 | 範例 |
|---------|------|------|
| `product_id` | 產品唯一識別碼 | "TOUR001" |
| `product_name` | 產品名稱 | "東京迪士尼樂園一日遊" |
| `product_location_country` | 產品所在國家 | "日本" |
| `price` | 產品價格 | 2500.00 |

### 支援格式
- **CSV**: UTF-8、Big5、GBK 編碼
- **Excel**: .xlsx、.xls 格式
- **檔案大小**: 建議不超過 10MB

### 資料品質檢查
系統會自動檢查並提醒：
- ✅ 必要欄位完整性
- ✅ 重複產品 ID
- ✅ 空白產品名稱
- ✅ 異常價格數據

## 🔧 技術架構

### 核心技術棧
- **🎨 前端框架**: Streamlit 1.28+
- **📊 資料處理**: Pandas + NumPy
- **🔄 翻譯服務**: Deep-Translator (Google Translate)
- **📈 視覺化**: Plotly Interactive Charts
- **☁️ 雲端平台**: Google Cloud Run
- **🐳 容器化**: Docker with Python 3.11

### 演算法核心
```python
def calculate_jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
    """計算 Jaccard 相似度: |A∩B| / |A∪B|"""
    intersection = set1 & set2
    union = set1 | set2
    return len(intersection) / len(union) if union else 0
```

### 效能優化
- **翻譯快取**: 避免重複翻譯相同文字
- **批次處理**: 最佳化大量產品比對
- **進度追蹤**: 即時顯示處理進度
- **記憶體管理**: 分段處理大型檔案

## 📈 使用流程

### 步驟 1: 檔案上傳
1. 點選「📁 檔案上傳」分頁
2. 分別上傳供應商 A 和 B 的產品檔案
3. 系統自動驗證檔案格式和必要欄位

### 步驟 2: 資料預覽
1. 切換到「👀 資料預覽」分頁
2. 檢查前 10 筆資料確認格式正確
3. 查看資料摘要和品質報告

### 步驟 3: 參數設定
1. 在側邊欄調整比對參數：
   - **相似度門檻**: 0.1-1.0 (建議 0.2-0.5)
   - **詞彙差異限制**: 防止長短差異過大的產品比對
   - **翻譯選項**: 是否啟用自動翻譯

### 步驟 4: 執行比對
1. 點選「🔍 執行比對」分頁
2. 點擊「🚀 開始比對」按鈕
3. 系統顯示即時進度和處理狀態

### 步驟 5: 結果分析
1. 切換到「📊 結果分析」查看：
   - 📊 關鍵指標統計
   - 📈 視覺化圖表分析
   - 🌍 按國家統計
   - 🏆 相似度排行榜

### 步驟 6: 匯出結果
1. 選擇匯出格式 (CSV 或 Excel)
2. 下載包含完整比對結果的檔案
3. 檔案自動加入時間戳記

## 🛡️ 系統需求

### 最低需求
- **作業系統**: Windows 10+ / macOS 10.14+ / Linux Ubuntu 18+
- **Python**: 3.8 或以上版本
- **記憶體**: 2GB RAM
- **儲存空間**: 1GB 可用空間
- **網路**: 穩定的網際網路連線 (翻譯功能需要)

### 建議配置
- **記憶體**: 4GB+ RAM (處理大型檔案)
- **處理器**: 雙核心 2.0GHz+ (提升處理速度)
- **瀏覽器**: Chrome 90+ / Firefox 88+ / Safari 14+

## 🔒 安全性與隱私

### 資料保護
- **本機處理**: 所有檔案處理均在本機或私有雲端進行
- **無資料儲存**: 系統不會永久儲存上傳的檔案
- **Session 隔離**: 每次使用完畢自動清除暫存資料

### 存取控制
- **密碼保護**: 企業級存取控制機制
- **Session 管理**: 24小時自動過期
- **使用追蹤**: 紀錄使用次數和時間

### 翻譯服務
- **API 安全**: 使用 HTTPS 加密傳輸
- **快取機制**: 減少外部 API 呼叫次數
- **錯誤處理**: 翻譯失敗時自動降級處理

## 🐛 疑難排解

### 常見問題

**Q: 無法啟動應用程式**
```bash
# 檢查 Python 版本
python --version

# 重新安裝依賴
pip install -r requirements.txt --force-reinstall
```

**Q: 檔案上傳失敗**
- 確認檔案格式為 CSV 或 Excel
- 檢查檔案大小不超過 10MB
- 驗證必要欄位是否存在

**Q: 翻譯功能異常**
- 確認網路連線正常
- 檢查是否有防火牆阻擋
- 可嘗試清除翻譯快取

**Q: 記憶體不足錯誤**
- 關閉其他不必要的程式
- 分批處理大型檔案
- 增加系統記憶體

### 錯誤日誌
系統會自動記錄錯誤資訊，位置：
- **本機**: 終端機輸出
- **雲端**: Google Cloud Logging

## 📞 技術支援

### 回報問題
如遇到問題，請提供以下資訊：
1. **錯誤訊息**: 完整的錯誤訊息截圖
2. **環境資訊**: 作業系統、Python 版本
3. **檔案資訊**: 檔案格式、大小、欄位名稱
4. **重現步驟**: 詳細的操作步驟

### 功能建議
歡迎提出功能改進建議：
- 新的比對算法
- 額外的檔案格式支援
- 更多的視覺化圖表
- 效能優化建議

## 📄 授權資訊

本專案採用 MIT 授權條款，詳見 [LICENSE](LICENSE) 檔案。

---

## 📝 更新日誌

### v1.0.0 (2025-08-08)
- 🎉 **首次發布**
- ✨ 完整的產品比對功能
- 🔒 企業級密碼保護
- ☁️ Google Cloud Run 部署
- 📊 豐富的視覺化分析
- 🌐 中英文智慧翻譯
- 💾 多格式結果匯出

---

<div align="center">

**🌟 如果這個專案對你有幫助，請給我們一個 Star！**

Made with ❤️ by EZTravel Team

</div>
